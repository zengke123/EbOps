# 数据获取接口
import datetime
from . import tongji
from .. import db
from flask import current_app, jsonify
from flask_login import login_required
from sqlalchemy import create_engine

engine = None
def exe_sql(sql):
    # 创建engine 连接tongji库
    global engine
    if not engine:
        engine = create_engine(current_app.config['SQLALCHEMY_BINDS']['tongji'], pool_recycle=3600)
        print('Connect mysql database tongji...')
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
    nowtime = (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
    data = {
        'scpas': get_scpas(nowtime),
        'catas': get_catas(nowtime),
        'scim': get_scim(nowtime),
        'sicp': get_sicp(nowtime)
    }
    print(data)
    return jsonify(data)


@tongji.route("/api/caps")
@login_required
def get_caps():
    caps_sql = "select `date`,`scpas_caps`,`catas_caps`,`vrbt_caps`,`scim_caps`,`ctx_caps` from caps " \
               "where date_sub(curdate(), INTERVAL 15 DAY) <= date(`date`);"
    datas = exe_sql(caps_sql)
    date = [int(x[0]) for x in datas]
    scpas_caps = [x[1] for x in datas]
    catas_caps = [x[2] for x in datas]
    vrbt_caps = [x[3] for x in datas]
    scim_caps = [x[4] for x in datas]
    ctx_caps = [x[5] for x in datas]
    data = [
        ['date', *date],
        ['SCPAS', *scpas_caps],
        ['音频彩铃', *catas_caps],
        ['视频彩铃', *vrbt_caps],
        ['SCIM', *scim_caps],
        ['Centrex', *ctx_caps],

    ]
    print(data)
    return jsonify(data)


def get_time_range(now, delta_minute):
    # 转为datetime格式，用于日期计算，str格式无法计算
    begin_date = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S") - datetime.timedelta(minutes=delta_minute)
    dates = []
    dt = begin_date
    date = begin_date.strftime("%Y-%m-%d %H:%M:%S")
    while date < now:
        dates.append(date)
        dt = dt + datetime.timedelta(minutes=1)
        date = dt.strftime("%Y-%m-%d %H:%M:%S")
    return dates


def get_chrg4g_service(service):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:00")
    # new = datetime.datetime.strptime(now_time, "%Y-%m-%d %H:%M:%S") - datetime.timedelta(days=2)
    # now = new.strftime("%Y-%m-%d %H:%M:%S")
    time_range = get_time_range(now_time, delta_minute=15)
    data = []
    for mo_dn in ("SCPAS03", "SCPAS04", "SCPAS05", "SCPAS06", "SCPAS07", "SCPAS08", "SCPAS35", "SCPAS38"):
        mo_dn_data = [mo_dn]

        # sql = "select * from node_chrg where date_sub(now(), INTERVAL 15 MINUTE)<= check_time " \
        #       "and network='4G' and service='{}' and mo_dn='{}';".format(service, mo_dn)
        sql = "select increment from node_chrg where check_time>='{}'  and check_time<='{}' "\
              "and network='4G' and service='{}' and mo_dn='{}';".format(time_range[0], time_range[-1], service, mo_dn)
        result = exe_sql(sql)
        for x in result:
            mo_dn_data.append(x[0])
        data.append(mo_dn_data)
    data.insert(0, ['时间', *time_range])
    return data


@tongji.route("/api/chrg4g")
@login_required
def get_chrg4g():
    vpmn_data = get_chrg4g_service('VPMN')
    home_data = get_chrg4g_service('HOME')
    frid_data = get_chrg4g_service('FRID')
    result = {
        'VPMN': vpmn_data,
        'HOME': home_data,
        'FRID': frid_data
    }
    # print(result)
    return jsonify(result)

