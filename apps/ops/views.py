from . import ops
from .. import db
from ..models import OpsItem, OpsInfo
from flask import render_template, request, jsonify
from flask_login import login_required


@ops.route("/ims",methods=['GET','POST'])
@login_required
def ims():
    _ops_items = db.session.query(OpsItem.c_name).filter(OpsItem.t_name == 'ims').all()
    _ops_infos = db.session.query(OpsInfo.id, OpsInfo.content, OpsInfo.cycle).filter(OpsInfo.t_name == 'ims').all()
    ops_item = _ops_items[0][0]
    return render_template('ops_ims.html', app='作业计划', action=ops_item, ops_item=ops_item, ops_infos=_ops_infos)


@ops.route("/sec",methods=['GET','POST'])
@login_required
def sec():
    _ops_items = db.session.query(OpsItem.c_name).filter(OpsItem.t_name == 'sec').all()
    _ops_infos = db.session.query(OpsInfo.id, OpsInfo.content, OpsInfo.cycle).filter(OpsInfo.t_name == 'sec').all()
    ops_item = _ops_items[0][0]
    return render_template('ops_ims.html', app='作业计划', action=ops_item, ops_item=ops_item, ops_infos=_ops_infos)


@ops.route("/vpmn",methods=['GET','POST'])
@login_required
def vpmn():
    _ops_items = db.session.query(OpsItem.c_name).filter(OpsItem.t_name == 'vpmn').all()
    _ops_infos = db.session.query(OpsInfo.id, OpsInfo.content, OpsInfo.cycle).filter(OpsInfo.t_name == 'vpmn').all()
    ops_item = _ops_items[0][0]
    return render_template('ops_ims.html', app='作业计划', action=ops_item, ops_item=ops_item, ops_infos=_ops_infos)


@ops.route("/vss",methods=['GET','POST'])
@login_required
def vss():
    _ops_items = db.session.query(OpsItem.c_name).filter(OpsItem.t_name == 'vss').all()
    _ops_infos = db.session.query(OpsInfo.id, OpsInfo.content, OpsInfo.cycle).filter(OpsInfo.t_name == 'vss').all()
    ops_item = _ops_items[0][0]
    return render_template('ops_ims.html', app='作业计划', action=ops_item, ops_item=ops_item, ops_infos=_ops_infos)


@ops.route("/cl",methods=['GET','POST'])
@login_required
def cl():
    _ops_items = db.session.query(OpsItem.c_name).filter(OpsItem.t_name == 'cl').all()
    _ops_infos = db.session.query(OpsInfo.id, OpsInfo.content, OpsInfo.cycle).filter(OpsInfo.t_name == 'cl').all()
    ops_item = _ops_items[0][0]
    return render_template('ops_ims.html', app='作业计划', action=ops_item, ops_item=ops_item, ops_infos=_ops_infos)


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
    with open(os.path.join(filepath, filename), encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            result += line + '\r\n'
        f.close()
    logs = {
        "data": result,
        "end": True,
        "mark": "7bbfef0c-103d-4b4f-8f43-39e7121db223"
    }
    return jsonify(logs)