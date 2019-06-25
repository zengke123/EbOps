from . import api_1
from .. import db
from .controllers import OpsEventHandler, OpsResultHandler
from flask import jsonify, request


# HTTP 方法   URL                                                    动作
# ==========  ===============================================        ==============================
# GET         http://[ip]:[port]/api/v1/tasks                        检索任务列表 ops_result
# GET         http://[ip]:[port]/api/v1/tasks/[task_id]              检索某个任务 ops_result
# GET         http://[ip]:[port]/api/v1/tasks/info/[task_id]         检索某个任务 ops_event
# POST        http://[ip]:[port]/api/v1/tasks                        创建新任务结果 ops_result
# POST        http://[ip]:[port]/api/v1/tasks/info                   创建新任务明细 ops_event
# PUT         http://[ip]:[port]/api/v1/tasks/[task_id]              更新任务 ops_result
# PUT         http://[ip]:[port]/api/v1/tasks/info/[task_id]         更新任务 ops_event
# DELETE      http://[ip]:[port]/api/v1/tasks/[task_id]              删除任务 ops_result
# DELETE      http://[ip]:[port]/api/v1/tasks/info/[task_id]         删除任务 ops_event


# 检索任务列表 ops_result
@api_1.route("/tasks")
def get_all_tasks():
    tasks = OpsResultHandler.listall()
    result = []
    for task in tasks:
        result.append(task.to_json())
    return jsonify({'result': 'success', 'message': result})


# 检索某个任务 ops_result
@api_1.route("/tasks/<task_id>")
def get_tasks(task_id):
    tasks = OpsResultHandler.list(task_id)
    if len(tasks) >= 1:
        result = []
        for task in tasks:
            result.append(task.to_json())
        return jsonify({'result': 'success', 'message': result})
    else:
        return jsonify({'result': 'fail', 'message': ''})


# 检索某个任务 ops_event
@api_1.route("/tasks/info/<task_id>")
def get_tasks_info(task_id):
    tasks = OpsEventHandler.list(task_id)
    if len(tasks) >= 1:
        result = []
        for task in tasks:
            result.append(task.to_json())
        return jsonify({'result': 'success', 'message': result})
    else:
        return jsonify({'result': 'fail', 'message': ''})


# 创建新任务结果 ops_result
@api_1.route("/tasks", methods=['POST'])
def create_tasks():
    req = request.get_json()
    result = OpsResultHandler.create(req)
    if result.get('flag'):
        return jsonify({'result': 'success', 'message': 'create success'})
    else:
        return jsonify({'result': 'fail', 'message': result.get('message')})


# 创建新任务明细 ops_event
@api_1.route("/tasks/info", methods=['POST'])
def create_tasks_event():
    req = request.get_json()
    result = OpsEventHandler.create(req)
    if result.get('flag'):
        return jsonify({'result': 'success', 'message': 'create success'})
    else:
        return jsonify({'result': 'fail', 'message': result.get('message')})


# 更新任务 ops_result
@api_1.route("/tasks/<task_id>", methods=['PUT'])
def update_tasks(task_id):
    req = request.get_json()
    result = OpsResultHandler.update(task_id, req)
    if result.get('flag'):
        return jsonify({'result': 'success', 'message': 'update success'})
    else:
        return jsonify({'result': 'fail', 'message': result.get('message')})


# 更新任务 ops_event
@api_1.route("/tasks/info/<task_id>", methods=['PUT'])
def update_tasks_event(task_id):
    req = request.get_json()
    result = OpsEventHandler.update(task_id, req)
    if result.get('flag'):
        return jsonify({'result': 'success', 'message': 'update success'})
    else:
        return jsonify({'result': 'fail', 'message': result.get('message')})


# 删除任务 ops_result
@api_1.route("/tasks/<task_id>", methods=['DELETE'])
def delete_tasks(task_id):
    result = OpsResultHandler.delete(task_id)
    if result.get('flag'):
        return jsonify({'result': 'success', 'message': 'delete success'})
    else:
        return jsonify({'result': 'fail', 'message': result.get('message')})


# 删除任务 ops_event
@api_1.route("/tasks/info/<task_id>", methods=['DELETE'])
def delete_tasks_event(task_id):
    result = OpsEventHandler.delete(task_id)
    if result.get('flag'):
        return jsonify({'result': 'success', 'message': 'delete success'})
    else:
        return jsonify({'result': 'fail', 'message': result.get('message')})

