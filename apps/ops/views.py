from . import ops
from .. import db
from ..models import OpsItem, OpsInfo, OpsResult
from datetime import datetime
from sqlalchemy import and_
from flask import render_template, request, jsonify
from flask_login import login_required


def get_result(ops_infos, date):
    results = []
    for item in ops_infos:
        # 根据item_id和date匹配执行结果，并按时间排序，取当天最后执行时间
        result = OpsResult.query.filter(and_(OpsResult.item_id == item.item_id,
                                             OpsResult.date == date)).order_by(OpsResult.time.desc()).first()
        results.append((item, result))
    return results


@ops.route("/<ops_type>", methods=['GET', 'POST'])
@login_required
def index(ops_type):
    # 查找ims对应的作业计划名称
    _ops_items = db.session.query(OpsItem.c_name).filter(OpsItem.t_name == ops_type).all()
    # 查找具体作业计划执行项
    _ops_infos = OpsInfo.query.filter(OpsInfo.t_name == ops_type).order_by(OpsInfo.id).all()
    ops_item = _ops_items[0][0]
    # 判断请求中是否带有日期，不带日期默认为当天
    if request.args.get('date_from'):
        date = request.args.get('date_from')
    else:
        date = datetime.now().strftime('%Y%m%d')
    # 根据日期和作业计划项item_id 获取执行记录
    _ops_results = get_result(_ops_infos, date)
    return render_template('ops_ims.html', app='作业计划', action=ops_item, ops_item=ops_item, ops_results=_ops_results)


# @ops.route("/sec",methods=['GET','POST'])
# @login_required
# def sec():
#     _ops_items = db.session.query(OpsItem.c_name).filter(OpsItem.t_name == 'sec').all()
#     _ops_infos = db.session.query(OpsInfo.id, OpsInfo.content, OpsInfo.cycle).filter(OpsInfo.t_name == 'sec').all()
#     ops_item = _ops_items[0][0]
#     return render_template('ops_item.html', app='作业计划', action=ops_item, ops_item=ops_item, ops_infos=_ops_infos)
#
#
# @ops.route("/vpmn",methods=['GET','POST'])
# @login_required
# def vpmn():
#     _ops_items = db.session.query(OpsItem.c_name).filter(OpsItem.t_name == 'vpmn').all()
#     _ops_infos = db.session.query(OpsInfo.id, OpsInfo.content, OpsInfo.cycle).filter(OpsInfo.t_name == 'vpmn').all()
#     ops_item = _ops_items[0][0]
#     return render_template('ops_item.html', app='作业计划', action=ops_item, ops_item=ops_item, ops_infos=_ops_infos)
#
#
# @ops.route("/vss",methods=['GET','POST'])
# @login_required
# def vss():
#     _ops_items = db.session.query(OpsItem.c_name).filter(OpsItem.t_name == 'vss').all()
#     _ops_infos = db.session.query(OpsInfo.id, OpsInfo.content, OpsInfo.cycle).filter(OpsInfo.t_name == 'vss').all()
#     ops_item = _ops_items[0][0]
#     return render_template('ops_item.html', app='作业计划', action=ops_item, ops_item=ops_item, ops_infos=_ops_infos)
#
#
# @ops.route("/cl",methods=['GET','POST'])
# @login_required
# def cl():
#     _ops_items = db.session.query(OpsItem.c_name).filter(OpsItem.t_name == 'cl').all()
#     _ops_infos = db.session.query(OpsInfo.id, OpsInfo.content, OpsInfo.cycle).filter(OpsInfo.t_name == 'cl').all()
#     ops_item = _ops_items[0][0]
#     return render_template('ops_item.html', app='作业计划', action=ops_item, ops_item=ops_item, ops_infos=_ops_infos)


@ops.route("/log/<log_id>")
@login_required
def ops_log(log_id):
    return render_template('ops_log.html',log_id=log_id)


@ops.route("/req")
@login_required
def request_log():
    import os
    log_id = request.args.get('log_id')
    filepath = '/Users/EB/PycharmProjects/EbOps'
    filename = log_id + '.txt'
    result = ''
    try:
        with open(os.path.join(filepath, filename), encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                result += line + '\r\n'
            f.close()
    except Exception as e:
        result = "\n日志文件不存在"
    logs = {
        "data": result,
        "end": True,
        "mark": "7bbfef0c-103d-4b4f-8f43-39e7121db223"
    }
    return jsonify(logs)