from . import check
from .. import db
from ..models import CheckHistory
from flask import render_template, request, jsonify, send_from_directory
from flask_login import login_required, current_user
from .exts import test_check, down_report
from .settings import DOWNLOAD_FOLDER

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
    r_clustername = request.args.get('clustername', None)
    r_hostname = request.args.get('hostname', None)
    if r_clustername:
        hostname = r_clustername
        host_type = "jq"
    else:
        hostname = r_hostname
        host_type = "zj"
    return render_template('check_confirm.html', app="自动例检", action="例检确认",
                           hostname=hostname, host_type=host_type)


# 自动例检主函数
@check.route('/autocheck', methods=['POST'])
@login_required
def autocheck_run():
    hostname = request.form.get('hostname')
    host_type = request.form.get('type')
    seed = request.form.get("seed")
    status[seed] = 20
    try:
        flag, result = test_check(host_type, hostname)
    except:
        flag = "fail"
        result = "WEB后台例检模块异常"
    status[seed] = 80
    import time
    time.sleep(5)
    # 例检成功，添加到历史记录
    if flag == "success":
        # report_name = down_report()
        report_name = '20190705112'
        new_type = "集群" if host_type == "jq" else "主机"
        add_log = CheckHistory(checktime=report_name, hostname=hostname, type=new_type, operator=current_user.username)
        db.session.add(add_log)
        db.session.commit()
    else:
        report_name = "null"
    status[seed] = 100
    status.pop(seed)
    return jsonify({'flag': flag, 'filename': "123456", 'lj_result': result})


# 获取例检状态,实现前端进度条
@check.route('/autocheck_status/<id>', methods=['GET', 'POST'])
def autocheck_status(id):
    seed = request.form.get("seed")
    return str(status.get(seed))


# 下载例检报告
@check.route('/download/<file>')
def download(file):
    filepath = DOWNLOAD_FOLDER + str(file) + '/'
    filename = str(file) + ".tar.gz"
    return send_from_directory(filepath, filename, as_attachment=True)
