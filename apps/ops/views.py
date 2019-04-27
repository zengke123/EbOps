from . import ops
from .. import db
from ..models import OpsItem, OpsInfo
from flask import render_template
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