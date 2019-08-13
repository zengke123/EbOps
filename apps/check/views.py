from . import check
from .. import db
from ..models import CheckHistory, CheckHost
from flask import render_template, request, jsonify, send_from_directory
from flask_login import login_required, current_user
from .exts import auto_check, down_report, req_zjlj
from werkzeug.utils import secure_filename
from ..settings import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, TEMPLATE_FOLDER, CHECK_DOWNLOAD_FOLDER
# 例检状态全局变量
status = {}


@check.route("/info", methods=['GET', 'POST'])
@login_required
def info():
    return render_template('check_list.html', app="自动例检", action="主机例检")


@check.route("/history", methods=['GET', 'POST'])
@login_required
def history():
    # 获取get请求传过来的页数,没有传参数，默认为1
    page = int(request.args.get('page', 1))
    date = request.args.get('date')
    if date and date != 'None':
        paginate = CheckHistory.query.filter(CheckHistory.checktime.like(date+'%')).order_by(CheckHistory.id.asc()).paginate(page, per_page=10, error_out=False)
    else:
        paginate = CheckHistory.query.order_by(CheckHistory.id.asc()).paginate(page, per_page=10, error_out=False)
    datas = paginate.items
    return render_template('check_history.html', app="自动例检", action="例检记录", paginate=paginate, datas=datas, date=date)


@check.route("/lj", methods=['GET', 'POST'])
@login_required
def check_host():
    _args = request.form.get('item_id', None)
    names = _args.split('_')
    print(names)
    if len(names) == 2:
        host_type = names[0]
        hostname = names[1]
        api_name = {'type':host_type, 'name':hostname}
        zjlj_task = req_zjlj.delay(api_name, hostname, current_user.username)
        return jsonify({'flag': 'success', 'desc': '任务已添加[id:{}]'.format(zjlj_task.id)})
    else:
        return jsonify({'flag': 'fail', 'desc': '参数错误'})
    # return render_template('check_confirm.html', app="自动例检", action="例检确认",
    #                        hostname=hostname, host_type=host_type)


# 自动例检主函数
@check.route('/autocheck', methods=['POST'])
@login_required
def autocheck_run():
    hostname = request.form.get('hostname')
    host_type = request.form.get('type')
    seed = request.form.get("seed")
    status[seed] = 20
    try:
        flag, result = auto_check(host_type, hostname)
    except:
        flag = "fail"
        result = "WEB后台例检模块异常"
    status[seed] = 80
    import time
    time.sleep(5)
    # 例检成功，添加到历史记录
    if flag == "success":
        report_name = down_report()
        # report_name = '20190705112'
        new_type = "集群" if host_type == "jq" else "主机"
        add_log = CheckHistory(checktime=report_name, hostname=hostname, type=new_type, operator=current_user.username)
        db.session.add(add_log)
        db.session.commit()
    else:
        report_name = "null"
    status[seed] = 100
    status.pop(seed)
    return jsonify({'flag': flag, 'filename': report_name, 'lj_result': result})


# 获取例检状态,实现前端进度条
@check.route('/autocheck_status/<id>', methods=['GET', 'POST'])
def autocheck_status(id):
    seed = request.form.get("seed")
    return str(status.get(seed))


# 下载例检报告
@check.route('/download/<file>')
def download(file):
    filepath = CHECK_DOWNLOAD_FOLDER + str(file) + '/'
    filename = str(file) + ".tar.gz"
    return send_from_directory(filepath, filename, as_attachment=True)


# 例检配置
@check.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    if request.method == "GET":
        return render_template('check_config.html', app="自动例检", action="例检配置")
    elif request.method == "POST":
        data = request.form.to_dict()
        print(data)
        add_host = CheckHost(**data)
        db.session.add(add_host)
        db.session.commit()
        info = "创建成功"
        return render_template('check_set_success.html', app="自动例检", action="例检配置", info=info)


# 批量导入例检配置
@check.route('/config/load', methods=['GET', 'POST'])
@login_required
def load_config():
    return render_template('check_load.html', app="自动例检", action="例检配置")


# 下载导入例检主机模板
@check.route('/down_templates')
@login_required
def down_templates():
    filename = 'check_data.xlsx'
    return send_from_directory(TEMPLATE_FOLDER, filename=filename, as_attachment=True)


# 资产导入模板允许文件
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 导入例检主机
@check.route('/fm_import', methods=["GET", "POST"])
@login_required
def fm_import():
    import os
    if request.method == 'POST':
        # 请求中无文件
        if 'file' not in request.files:
            return jsonify({'flag': 'fail', 'msg': '上传文件失败'})
        file = request.files['file']
        # 文件名为空
        if file.filename == '':
            return jsonify({'flag': 'fail', 'msg': '文件名错误'})
        # 文件符合要求
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # 调用入库函数
            nums = load_to_db(UPLOAD_FOLDER + filename)
            return jsonify({'flag': 'success', 'msg': '导入成功' + str(nums)})
        else:
            return jsonify({'flag': 'fail', 'msg': '上传文件格式错误'})


# 导入资产入库
def load_to_db(filename):
    from openpyxl import load_workbook
    nums = 0
    # 与数据中字段一致
    host_names = ["os", "pt", "jq", "zj", "zh", "jctype", "jcnum", "ip"]
    infos = {
        "cols": host_names,
        "sheet": "hosts"
        }
    try:
        wb = load_workbook(filename)
        # 读取导入excel文件中的sheet表
        ws = wb[infos.get("sheet")]
        # 获取列数
        cols = len(infos.get("cols"))
        # 获取行数
        rows = ws.max_row
        dbs = []
        # 读取excel中每行数据，构造成dict, 方便入库
        for i in range(2, rows + 1):
            data = []
            for j in range(1, cols + 1):
                value = ws.cell(i, j).value
                if not value:
                    value = ""
                data.append(value)
            item = {k: v for k, v in zip(infos.get("cols"), data)}
            dbs.append(CheckHost(**item))
        # 批量添加
        db.session.add_all(dbs)
        db.session.commit()
        nums = len(dbs)
    except Exception as e:
        print(str(e))
    finally:
        # 最后删除上传的文件
        import os
        os.remove(filename)
    return nums


# 删除设备
@check.route('/delete', methods=["GET", "POST"])
@login_required
def delete():
    hostname = request.form.get('id')
    try:
        to_deletes = CheckHost.query.filter(CheckHost.zj == hostname).all()
        for to_delete in to_deletes:
            db.session.delete(to_delete)
        db.session.commit()
        result = {"flag": "success"}
    except Exception as e:
        print(str(e))
        result = {"flag": "fail"}
    return jsonify(result)


# 批量删除设备
@check.route('/multi_delete', methods=["GET", "POST"])
@login_required
def multi_delete():
    _hosts = request.form.get('hosts')
    _hosts_temp = _hosts.split(',')
    # 去除checkbox选择的无效选项
    _hosts_list = [x for x in _hosts_temp if x != '' and x != 'on']
    if _hosts_list:
        for hostname in _hosts_list:
            to_deletes = CheckHost.query.filter(CheckHost.zj == hostname).all()
            for to_delete in to_deletes:
                db.session.delete(to_delete)
        db.session.commit()
        return "success"
    else:
        return "fail"