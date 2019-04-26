from . import ops
from .. import db
from ..models import OpsItem, OpsInfoCl, OpsInfoIms, OpsInfoSec, OpsInfoVpmn, OpsInfoVss
from flask import render_template
from flask_login import login_required


@ops.route("/ims",methods=['GET','POST'])
@login_required
def ims():
    _ops_items = db.session.query(OpsItem.c_name).filter(OpsItem.t_name == 'ops_ims').all()
    _ops_infos = db.session.query(OpsInfoIms.id, OpsInfoIms.content, OpsInfoIms.cycle).all()
    ops_item = _ops_items[0][0]
    return render_template('ops_ims.html', app='作业计划', action=ops_item, ops_item=ops_item, ops_infos=_ops_infos)


@ops.route("/sec",methods=['GET','POST'])
@login_required
def sec():
    _ops_items = db.session.query(OpsItem.c_name).filter(OpsItem.t_name == 'ops_sec').all()
    _ops_infos = db.session.query(OpsInfoSec.id, OpsInfoSec.content, OpsInfoSec.cycle).all()
    ops_item = _ops_items[0][0]
    return render_template('ops_ims.html', app='作业计划', action=ops_item, ops_item=ops_item, ops_infos=_ops_infos)


@ops.route("/vpmn",methods=['GET','POST'])
@login_required
def vpmn():
    _ops_items = db.session.query(OpsItem.c_name).filter(OpsItem.t_name == 'ops_vpmn').all()
    _ops_infos = db.session.query(OpsInfoVpmn.id, OpsInfoVpmn.content, OpsInfoVpmn.cycle).all()
    ops_item = _ops_items[0][0]
    return render_template('ops_ims.html', app='作业计划', action=ops_item, ops_item=ops_item, ops_infos=_ops_infos)


@ops.route("/vss",methods=['GET','POST'])
@login_required
def vss():
    _ops_items = db.session.query(OpsItem.c_name).filter(OpsItem.t_name == 'ops_vss').all()
    _ops_infos = db.session.query(OpsInfoVss.id, OpsInfoVss.content, OpsInfoVss.cycle).all()
    ops_item = _ops_items[0][0]
    return render_template('ops_ims.html', app='作业计划', action=ops_item, ops_item=ops_item, ops_infos=_ops_infos)


@ops.route("/cl",methods=['GET','POST'])
@login_required
def cl():
    _ops_items = db.session.query(OpsItem.c_name).filter(OpsItem.t_name == 'ops_cl').all()
    _ops_infos = db.session.query(OpsInfoCl.id, OpsInfoCl.content, OpsInfoCl.cycle).all()
    ops_item = _ops_items[0][0]
    return render_template('ops_ims.html', app='作业计划', action=ops_item, ops_item=ops_item, ops_infos=_ops_infos)