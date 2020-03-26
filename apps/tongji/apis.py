# 数据获取接口
import datetime
from . import tongji
from .. import db
from flask import current_app, jsonify
from flask_login import login_required
from sqlalchemy import create_engine

def exe_sql(sql):
    # 创建engine 连接tongji库
    engine = create_engine(current_app.config['SQLALCHEMY_BINDS']['tongji'])
    print(sql)
    data = db.session.execute(sql, bind=engine).fetchall()
    return data


def get_data(nowtime, mo_dn_sql, time_sql):
    mo_dns = [x[0] for x in exe_sql(mo_dn_sql)]
    categories = [x[0] for x in exe_sql(time_sql)]
    categories.insert(0, 'mo_dn')
    source = [categories]
    for mo_dn in mo_dns:
        pfmc_sql = "SELECT succsessionrate FROM node_pfmc where mo_dn='{}' and end_time >= '{}'".format(mo_dn, nowtime)
        pfmc_data = [float(x[0]) for x in exe_sql(pfmc_sql)]
        pfmc_data.insert(0, mo_dn)
        source.append(pfmc_data)
    return source


def get_scpas(nowtime):
    # 获取scpas 数据
    mo_dn_sql = "SELECT DISTINCT(mo_dn) FROM node_pfmc where mo_dn like 'SCP-SCPAS%' and end_time >= '{}'".format(nowtime)
    time_sql = "SELECT DISTINCT(end_time) FROM node_pfmc where mo_dn like 'SCP-SCPAS%' and end_time >= '{}'".format(
        nowtime)
    source = get_data(nowtime, mo_dn_sql, time_sql)
    return source


def get_scp(nowtime):
    mo_dn_sql = "SELECT DISTINCT(mo_dn) FROM node_pfmc where mo_dn like 'SCP-SCP__' and end_time >= '{}'".format(nowtime)
    time_sql = "SELECT DISTINCT(end_time) FROM node_pfmc where mo_dn like 'SCP-SCP__' and end_time >= '{}'".format(
        nowtime)
    source = get_data(nowtime, mo_dn_sql, time_sql)
    return source


def get_catas(nowtime):
    mo_dn_sql = "SELECT DISTINCT(mo_dn) FROM node_pfmc where mo_dn like 'CRBT-CATAS%' and end_time >= '{}'".format(nowtime)
    time_sql = "SELECT DISTINCT(end_time) FROM node_pfmc where mo_dn like 'CRBT-CATAS%' and end_time >= '{}'".format(
        nowtime)
    source = get_data(nowtime, mo_dn_sql, time_sql)
    return source


def get_scim(nowtime):
    mo_dn_sql = "SELECT DISTINCT(mo_dn) FROM node_pfmc where mo_dn like 'SCP-SCIM%' and end_time >= '{}'".format(nowtime)
    time_sql = "SELECT DISTINCT(end_time) FROM node_pfmc where mo_dn like 'SCP-SCIM%' and end_time >= '{}'".format(
        nowtime)
    source = get_data(nowtime, mo_dn_sql, time_sql)
    return source


def get_sicp(nowtime):
    mo_dn_sql = "SELECT DISTINCT(mo_dn) FROM node_pfmc where mo_dn like 'SICP-SICP%' and end_time >= '{}'".format(nowtime)
    time_sql = "SELECT DISTINCT(end_time) FROM node_pfmc where mo_dn like 'SICP-SICP%' and end_time >= '{}'".format(
        nowtime)
    source = get_data(nowtime, mo_dn_sql, time_sql)
    return source

@tongji.route("/api/node_pfmc")
@login_required
def get_node_pfmc():
    nowtime = (datetime.datetime.now() - datetime.timedelta(hours=42)).strftime("%Y-%m-%d %H:%M:%S")
    data = {
        'scpas': get_scpas(nowtime),
        'catas': get_catas(nowtime),
        'scim': get_scim(nowtime),
        'sicp': get_sicp(nowtime)
    }
    print(data)
    return jsonify(data)