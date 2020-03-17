import os
import datetime
from . import file_manager
from .settings import DocPath
from .. import db
from ..models import FmCagetory, FmTags, FmFiles
from sqlalchemy import and_
from flask import render_template, request, jsonify, send_from_directory
from flask_login import login_required, current_user


@file_manager.route('/', methods=["GET", "POST"])
@login_required
def main():
    cagetory_temp = db.session.query(FmCagetory.cagetory).all()
    cagetory = [x[0] for x in cagetory_temp]
    tas_temp = db.session.query(FmTags.tags).all()
    tags = [x[0] for x in tas_temp]
    files = db.session.query(FmFiles).all()
    return render_template('fm_list.html', app='共享文档', cagetory=cagetory, tags=tags, files=files,
                           current_user=current_user)


# 上传文件
@file_manager.route('/upload', methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "GET":
        cagetory_temp = db.session.query(FmCagetory.cagetory).all()
        cagetory = [x[0] for x in cagetory_temp]
        tas_temp = db.session.query(FmTags.tags).all()
        tags = [x[0] for x in tas_temp]
        return render_template('fm_upload.html', app='共享文档', action="上传文件", cagetory=cagetory, tags=tags)
    elif request.method == "POST":
        req = request.form
        if 'file' not in request.files:
            return jsonify({'flag': 'fail', 'msg': '请选择文件'})
        tags = req.get('tags')[:-1] if req.get('tags') else ""
        file = request.files['file']
        filename = file.filename
        file.save(os.path.join(DocPath, filename))
        args = {
            'filename': filename,
            'cagetory': req.get('cagetory'),
            'tags': tags,
            'size': round(os.path.getsize(os.path.join(DocPath, filename))/float(1024),1),
            'owner': current_user.username,
            'update': datetime.datetime.now().strftime('%Y%m%d%H%M'),
            'downloads': 0,
        }
        print(args)
        try:
            db.session.add(FmFiles(**args))
            db.session.commit()
            return jsonify({'flag': 'success'})
        except Exception as e:
            print(str(e))
            return jsonify({'flag': 'fail', 'msg': str(e)})


# 上传文件
@file_manager.route('/conf', methods=["GET", "POST"])
@login_required
def conf():
    cagetory_temp = db.session.query(FmCagetory.cagetory).all()
    cagetory = [x[0] for x in cagetory_temp]
    tas_temp = db.session.query(FmTags.tags).all()
    tags = [x[0] for x in tas_temp]
    return render_template('fm_setting.html', app='共享文档', action="文件夹管理", cagetory=cagetory, tags=tags)


# 增加类别
@file_manager.route('/add_cagetory', methods=["POST"])
@login_required
def add_cagetory():
    req = request.form
    cagetory = req.get('cagetory')
    if not cagetory:
        return jsonify({'flag':'fail', 'desc': '名称不能为空'})
    try:
        db.session.add(FmCagetory(cagetory=cagetory))
        db.session.commit()
        return jsonify({'flag': 'success'})
    except Exception as e:
        desc = str(e)
        print(desc)
        return jsonify({'flag':'fail', 'desc': desc})


# 删除类别, 管理员权限
@file_manager.route('/del_cagetory', methods=["POST"])
@login_required
def del_cagetory():
    req = request.form
    cagetory = req.get('cagetory')
    try:
        if not current_user.is_admin:
            return jsonify({"flag": "fail", "msg":"无删除权限"})
        to_del = FmCagetory.query.filter(FmCagetory.cagetory == cagetory).first()
        db.session.delete(to_del)
        print(to_del)
        to_del_files = FmFiles.query.filter(FmFiles.cagetory == cagetory).all()
        print(to_del_files)
        # 该类别下已有文件
        if to_del_files:
            for file in to_del_files:
                # 删除表数据
                db.session.delete(file)
                # 删除原始文件
                filename = file.filename
                os.remove(os.path.join(DocPath, filename))
        db.session.commit()
        print(current_user.username, "DELETE FOLDERS " + cagetory)
        return jsonify({'flag': 'success'})
    except Exception as e:
        desc = str(e)
        print(desc)
        return jsonify({'flag':'fail', 'desc': desc})


# 修改类别
@file_manager.route('/update_cagetory', methods=["POST"])
@login_required
def update_cagetory():
    req = request.form
    old_cagetory = req.get('old')
    new_cagetory = req.get('new')
    if not new_cagetory:
        return jsonify({'flag': 'fail', 'desc': '名称不能为空'})
    try:
        to_update = FmCagetory.query.filter(FmCagetory.cagetory == old_cagetory).first()
        to_update.cagetory = new_cagetory
        to_update_files = FmFiles.query.filter(FmFiles.cagetory == old_cagetory).all()
        print(to_update)
        # 该类别下已有文件
        if to_update_files:
            for file in to_update_files:
               file.cagetory = new_cagetory
        db.session.commit()
        return jsonify({'flag': 'success'})
    except Exception as e:
        desc = str(e)
        print(desc)
        return jsonify({'flag':'fail', 'desc': desc})



# 增加标签
@file_manager.route('/add_tag', methods=["POST"])
@login_required
def add_tag():
    req = request.form
    tags = req.get('tags')
    if not tags:
        return jsonify({'flag':'fail', 'desc': '名称不能为空'})
    try:
        db.session.add(FmTags(tags=tags))
        db.session.commit()
        return jsonify({'flag': 'success'})
    except Exception as e:
        desc = str(e)
        print(desc)
        return jsonify({'flag':'fail', 'desc': desc})


# 删除标签
@file_manager.route('/del_tag', methods=["POST"])
@login_required
def del_tag():
    req = request.form
    tags = req.get('tags')
    try:
        if not current_user.is_admin:
            return jsonify({"flag": "fail", "msg": "无删除权限"})
        to_del = FmTags.query.filter(FmTags.tags == tags).first()
        db.session.delete(to_del)
        print(to_del)
        to_del_files = FmFiles.query.filter(FmFiles.tags.like('%{}%'.format(tags))).all()
        print(to_del_files)
        # 该类别下已有文件
        if to_del_files:
            for file in to_del_files:
                # 删除表数据
                db.session.delete(file)
                # 删除原始文件
                filename = file.filename
                os.remove(os.path.join(DocPath, filename))
        db.session.commit()
        print(current_user.username, "DELETE FOLDERS " + tags)
        return jsonify({'flag': 'success'})
    except Exception as e:
        desc = str(e)
        print(desc)
        return jsonify({'flag': 'fail', 'desc': desc})


# 修改类别
@file_manager.route('/update_tags', methods=["POST"])
@login_required
def update_tags():
    req = request.form
    old_tags = req.get('old')
    new_tags = req.get('new')
    if not new_tags:
        return jsonify({'flag': 'fail', 'desc': '名称不能为空'})
    try:
        to_update = FmTags.query.filter(FmTags.tags == old_tags).first()
        to_update.tags = new_tags
        to_update_files = FmFiles.query.filter(FmFiles.tags.like('%{}%'.format(old_tags))).all()
        print(to_update)
        # 该类别下已有文件
        if to_update_files:
            for file in to_update_files:
                # 文件对应多个标签，采用 replace 替换
                temp = file.tags
                file.tags = temp.replace(old_tags, new_tags)
        db.session.commit()
        return jsonify({'flag': 'success'})
    except Exception as e:
        desc = str(e)
        print(desc)
        return jsonify({'flag':'fail', 'desc': desc})



# 下载文件
@file_manager.route('/download/<id>')
@login_required
def download_file(id):
    current_file = FmFiles.query.filter(FmFiles.id == int(id)).first()
    filename = current_file.filename
    print(current_file.downloads)
    current_file.downloads += 1
    db.session.commit()
    return send_from_directory(DocPath, filename=filename, as_attachment=True)


#  删除文件
@file_manager.route('/delete', methods=["POST"])
@login_required
def delete_file():
    file_id = request.form.get('id')
    try:
        to_delete = FmFiles.query.filter(FmFiles.id == file_id).first()
        if to_delete.owner != current_user.username and not current_user.is_admin:
            return jsonify({"flag": "fail", "msg":"无删除权限"})
        filename = to_delete.filename
        db.session.delete(to_delete)
        db.session.commit()
        result = {"flag": "success"}
        # 删除原始文件
        os.remove(os.path.join(DocPath, filename))
    except Exception as e:
        print(str(e))
        result = {"flag": "fail"}
    return jsonify(result)


# 根据类别获取文件列表
@file_manager.route("/get_files_by_type", methods=['GET', 'POST'])
def get_by_type():
    cagetory = request.form.get('cagetory')
    files_temp = FmFiles.query.filter(FmFiles.cagetory == cagetory).all()
    result = []
    for i, host in enumerate(files_temp):
        result.append(host.to_json())
    return jsonify(result)


# 根据类别获取文件列表
@file_manager.route("/get_files_by_tags", methods=['GET', 'POST'])
def get_by_tags():
    cagetory = request.form.get('cagetory')
    tags = request.form.get('tags')
    # files_temp = FmFiles.query.filter(FmFiles.cagetory == cagetory).all()
    print(cagetory, tags)
    files_temp = db.session.query(FmFiles).filter(
        and_(FmFiles.cagetory==cagetory, FmFiles.tags.like("%{}%".format(tags)))).all()

    result = []
    for file in files_temp:
        result.append(file.to_json())

    return jsonify(result)