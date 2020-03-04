import os
import datetime
import requests
from . import operate
from .. import db
from ..models import User
from .settings import API_URL, AttachPath, DestPath
from flask import render_template, send_from_directory, request, jsonify
from flask_login import login_required, current_user


# 待办操作
@operate.route('/todo')
@login_required
def task_todo():
    user = current_user.username
    if current_user.is_admin:
        # 查看非本用户 所有状态为 Created, apply 及本用户创建的未完操作 状态为 permit
        resp = requests.get(API_URL + "operation/findall")
        temp = resp.json()
        result = []
        if isinstance(temp, list):
            for task in temp:
                if task.get('opStatus') == "Created" or task.get('opStatus') == "apply":
                    result.append(task)
                if task.get('opCreator') == user and task.get('opStatus') == "permit":
                    result.append(task)
    else:
        # 本用户状态不为 finished
        resp = requests.post(API_URL+"operation/findByOpCreator", json={'opCreator': user})
        temp = resp.json()
        result = []
        if isinstance(temp, list):
            for task in temp:
                if task.get('opStatus') != "finish":
                    result.append(task)
    # result = [
    #     {
    #         "id": 1,
    #         "opContent": "BEP204主机自重启，需要恢复数据库HDR",
    #         "opDetail": "1、启动BEP204数据库 informix@bep204：oninit -vy\n2、主库上备份数据库连接数 informix@bep205：onstat -g ses > sesbak0208\n3、将主库置为标准库 \ninformix@bep205：onmode -d standard\n4、进行数据库零备恢复：nohup ontape -s -L 0 -F|remsh bep204 \". ./.profile;ontape -p\" &\n5、待online日志中出现 Archive on rootdbs, logdbs, phydbs, userdbs, Completed 继续后续操作恢复hdr\nbep205>onmode -d primary hdr201\nbep204>onmode -d secondary hdr202\n检查是否成功搭建\n主库online.log出现“DR: Primary server operational”\n备库online.log出现“DR: HDR secondary server operational”\n主备库onstat -g dri看到的状态都正常\n6、启动gealarm",
    #         "opResult": "",
    #         "opNote": "",
    #         "opSubject": "SCP20数据库恢复HDR",
    #         "opSubsystem": "SCP20",
    #         "opAttachflag": "n",
    #         "opAttachname": "",
    #         "opAttachpath": "",
    #         "opPermit": "",
    #         "opType": "basic",
    #         "opCreator": "zengke",
    #         "opOperator": "曾科",
    #         "opStatus": "Created",
    #         "opPlanTime": "2020-02-08 23:59",
    #         "opCreateDate": "2020-02-19",
    #         "opCreateTime": "21:22:28",
    #         "opFinishDate": "2020-02-08",
    #         "opFinishTime": "18:05:47",
    #         "opTimeStamp": "null",
    #         "opOriginator": "none",
    #         "opOutReviewer": "",
    #         "opInReviewer": "",
    #         "opLocation": "4A"
    #     },
    #     {
    #         "id": 3,
    #         "opContent": "test",
    #         "opDetail": "test",
    #         "opResult": "",
    #         "opNote": "",
    #         "opSubject": "测试",
    #         "opSubsystem": "test",
    #         "opAttachflag": "n",
    #         "opAttachname": "",
    #         "opAttachpath": "",
    #         "opPermit": "",
    #         "opType": "basic",
    #         "opCreator": "zengke",
    #         "opOperator": "曾科",
    #         "opStatus": "Created",
    #         "opPlanTime": "2020-02-19 23:59",
    #         "opCreateDate": "2020-02-19",
    #         "opCreateTime": "23:52:29",
    #         "opFinishDate": "",
    #         "opFinishTime": "",
    #         "opTimeStamp": "null",
    #         "opOriginator": "none",
    #         "opOutReviewer": "",
    #         "opInReviewer": "",
    #         "opLocation": "4A"
    #     },
    #     {
    #         "id": 4,
    #         "opContent": "test",
    #         "opDetail": "1.qwe\r\n2.qwe\r\n3.qwe",
    #         "opResult": "",
    #         "opNote": "",
    #         "opSubject": "测试",
    #         "opSubsystem": "123",
    #         "opAttachflag": "n",
    #         "opAttachname": "",
    #         "opAttachpath": "",
    #         "opPermit": "",
    #         "opType": "basic",
    #         "opCreator": "zengke",
    #         "opOperator": "曾科",
    #         "opStatus": "Created",
    #         "opPlanTime": "2020-02-19 23:59",
    #         "opCreateDate": "2020-02-19",
    #         "opCreateTime": "23:56:59",
    #         "opFinishDate": "",
    #         "opFinishTime": "",
    #         "opTimeStamp": "null",
    #         "opOriginator": "none",
    #         "opOutReviewer": "",
    #         "opInReviewer": "",
    #         "opLocation": "4A"
    #     }
    # ]
    # 按状态分类
    # created_res = []
    # apply_res = []
    # permit_res = []
    # for item in result:
    #     if item.get('opStatus') == "Created":
    #         created_res.append(item)
    #     elif item.get('opStatus') == "apply":
    #         apply_res.append(item)
    #     elif item.get('opStatus') == "permit":
    #         permit_res.append(item)

    result.sort(key=lambda item: item.get('id'), reverse=True)
    return render_template('operate_todo.html', app="操作审批", action="待办", result=result, current_user=current_user)


# 新建操作
@operate.route('/create', methods=['GET', 'POST'])
@login_required
def task_create():
    if request.method == "GET":
        now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M")
        return render_template('operate_new.html', app="操作审批", action="新建", now=now)
    elif request.method == "POST":
        req = request.form
        body = {
            "opAttachflag": "n",
            "opAttachname": "",
            "opAttachpath": "",
            "opContent": req.get('opContent'),
            "opCreateDate": "",
            "opCreateTime": "",
            "opCreator": current_user.username,
            "opDetail": req.get('opDetail'),
            "opFinishDate": "",
            "opFinishTime": "",
            "opInReviewer": "",
            "opLocation": req.get('opLocation'),
            "opNote": "",
            "opOperator": req.get('opOperator'),
            "opOriginator": req.get('opOriginator'),
            "opOutReviewer": "",
            "opPermit": "",
            "opPlanTime": req.get('opPlanTime'),
            "opResult": "",
            "opStatus": "",
            "opSubject": req.get('opSubject'),
            "opSubsystem": req.get('opSubsystem'),
            "opTimeStamp": "",
            "opType": ""
        }
        if 'file' not in request.files:
            body['opAttachflag'] = 'n'
        else:
            file = request.files['file']
            filename = file.filename
            file.save(os.path.join(AttachPath, filename))
            body['opAttachflag'] = 'y'
            body['opAttachname'] = filename
            body['opAttachpath'] = DestPath
        print(body)

        result = requests.post(API_URL + "operation", json=body)
        if result.status_code == 200:
            print(result.json())
            return jsonify({'flag': 'success'})
        else:
            return jsonify({'flag': 'fail'})


# 操作审批详情
@operate.route('/detail/<id>')
@login_required
def task_detail(id):
    resp = requests.get(API_URL+"operation/" + id)

    # result = [
    #     {
    #         "id": 1,
    #         "opContent": "BEP204主机自重启，需要恢复数据库HDR",
    #         "opDetail": "1、启动BEP204数据库 informix@bep204：oninit -vy\n2、主库上备份数据库连接数 informix@bep205：onstat -g ses > sesbak0208\n3、将主库置为标准库 \ninformix@bep205：onmode -d standard\n4、进行数据库零备恢复：nohup ontape -s -L 0 -F|remsh bep204 \". ./.profile;ontape -p\" &\n5、待online日志中出现 Archive on rootdbs, logdbs, phydbs, userdbs, Completed 继续后续操作恢复hdr\nbep205>onmode -d primary hdr201\nbep204>onmode -d secondary hdr202\n检查是否成功搭建\n主库online.log出现“DR: Primary server operational”\n备库online.log出现“DR: HDR secondary server operational”\n主备库onstat -g dri看到的状态都正常\n6、启动gealarm",
    #         "opResult": "",
    #         "opNote": "",
    #         "opSubject": "SCP20数据库恢复HDR",
    #         "opSubsystem": "SCP20",
    #         "opAttachflag": "n",
    #         "opAttachname": "",
    #         "opAttachpath": "",
    #         "opPermit": "",
    #         "opType": "basic",
    #         "opCreator": "zengke",
    #         "opOperator": "曾科",
    #         "opStatus": "Created",
    #         "opPlanTime": "2020-02-08 23:59",
    #         "opCreateDate": "2020-02-19",
    #         "opCreateTime": "21:22:28",
    #         "opFinishDate": "2020-02-08",
    #         "opFinishTime": "18:05:47",
    #         "opTimeStamp": "null",
    #         "opOriginator": "none",
    #         "opOutReviewer": "",
    #         "opInReviewer": "",
    #         "opLocation": "4A"
    #     }
    # ]
    return render_template('operate_detail.html', app="操作审批", action="详情", result=resp.json(),
                           current_user=current_user)


# 操作记录
@operate.route('/all')
@login_required
def task_all():
    _all_users = db.session.query(User.username).all()
    users = [x[0] for x in _all_users]
    user = current_user.username
    if current_user.is_admin:
        resp_users = users
    else:
        resp_users = [user]
    resp = requests.post(API_URL+"operation/findByOpCreator", json={'opCreator': user})
    result = resp.json()
    result.sort(key=lambda item: item.get('id'), reverse=True)
    return render_template('operate_list.html', app="操作审批", action="操作记录", result=result,
                           current_user=current_user, users=resp_users)


# 更改 opStatus 状态对应名称及标签颜色
def status_map(task):
    map = {
        "Created": ("待内审", "label-warning"),
        "apply": ("待局审", "label-danger"),
        "permit": ("待操作", "label-success"),
        "finish": ("已完成", "label-default"),
        # 兼容历史状态
        "created": ("待内审", "label-warning"),
        "permitted": ("待操作", "label-success"),
        "finished": ("已完成", "label-default")
    }
    opStatus = task.get('opStatus')
    try:
        task['opStatus'] = map.get(opStatus)[0]
        task['color'] = map.get(opStatus)[1]
    except TypeError:
        task['color'] = "label-default"
    return task


# 搜索
@operate.route('/searcUser', methods=['GET', 'POST'])
@login_required
def user_search():
    req = request.form
    opStatus = req.get('opStatus')
    opCreator = req.get('opCreator')
    # 选择所有
    if opStatus == "all" and opCreator == "all":
        resp = requests.get(API_URL + "operation/findall")
        result = resp.json()
    # 根据状态筛选
    elif opStatus != "all" and opCreator == "all":
        body = {
            "opStatus": opStatus
        }
        print(body)
        resp = requests.post(API_URL + "operation/findByOpStatus", json=body)
        result = resp.json()
    # 根据用户筛选
    elif opStatus == "all" and opCreator != "all":
        body = {
            "opCreator": opCreator
        }
        print(body)
        resp = requests.post(API_URL + "operation/findByOpCreator", json=body)
        result = resp.json()
    else:
        body = {
            "opStatus": opStatus,
            "opCreator": opCreator
        }
        print(body)
        resp = requests.post(API_URL + "operation/findByOpCreatorAndOpStatus", json=body)
        result = resp.json()
    # print(result)
    # 映射状态名称
    search_result = list(map(status_map, result))
    # print(search_result)

    if current_user.is_admin:
        map_result = search_result
    else:
        map_result = []
        for item in search_result:
            if item.get('opCreator') == current_user.username:
                map_result.append(item)

    map_result.sort(key=lambda item: item.get('id'), reverse=True)
    return jsonify({'flag': 'success','datas': map_result, 'counts': len(map_result)})
    # return jsonify(result)


# 搜索
@operate.route('/search', methods=['GET', 'POST'])
@login_required
def task_search():
    req = request.form
    opContent = req.get('opContent')
    body = {
        "content": opContent
    }
    resp = requests.post(API_URL + "operation/search", json=body)
    result = resp.json()
    # 映射状态名称
    map_result = list(map(status_map, result))
    if current_user.is_admin:
        search_result = map_result
    else:
        search_result =[]
        for item in map_result:
            if item.get('opCreator') == current_user.username:
                search_result.append(item)
    print(search_result)
    search_result.sort(key=lambda item: item.get('id'), reverse=True)
    return jsonify({'flag': 'success','datas': search_result, 'counts': len(search_result)})


@operate.route('/action', methods=['GET', 'POST'])
@login_required
def task_action():
    req = request.form
    print(req)
    id_action = req.get('action')
    id = id_action.split('|')[0]
    action = id_action.split('|')[1]
    opResult = req.get('opResult', '')
    outReviewer = req.get('outReviewer', '')
    body = {
        "user": current_user.username,
        "action": action,
        "outReviewer": outReviewer,
        "opResult": opResult
    }
    print(id)
    print(body)
    resp = requests.post(API_URL + "operation/" + id, json=body)
    result = resp.json()
    print(result)
    if result.get('result') == "Succeed":
        return jsonify({'flag': 'success'})
    else:
        return jsonify({'flag': 'fail'})
    # return jsonify({'flag': 'success'})


@operate.route('/download/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(AttachPath, filename=filename, as_attachment=True)