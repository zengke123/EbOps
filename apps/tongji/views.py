import datetime
from . import tongji
from .. import db
from flask import render_template, current_app, request
from flask_login import login_required
from sqlalchemy import create_engine


@tongji.route('/data')
@login_required
def profiledata():
    # 获取前台提交的日期，若无，默认使用前一天日期
    date = request.args.get('date', '')
    engine = create_engine(current_app.config['SQLALCHEMY_BINDS']['tongji'])
    if not date:
        date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    # 获取前一天的日期，用于同比计算
    before_date = (datetime.datetime.strptime(date, '%Y%m%d') - datetime.timedelta(days=1)).strftime("%Y%m%d")

    # 查询指标函数
    def query_zb(_items: list, _date):
        # 查询相关字段对应日期的结果
        sql = "select {} from ywzb where date={}".format(','.join(_items), _date)
        _data = db.session.execute(sql.format(date, date), bind=engine).fetchall()
        # 查询结果不为空
        if _data:
            # 将_items和查询结果对应，转成dict
            _data_dict = dict(zip(_items, _data[0]))
            return _data_dict
        else:
            # 查询结果为空时，使用空替代
            _data_dict = dict(zip(_items, ["" for _ in range(len(_items))]))
            return _data_dict

    # 数据库中业务指标对应的字段
    scp_items = ['2gscp_minsucc', '2gscp_minsucc_cluster', '2gscp_maxcaps', '2gscp_maxcaps_cluster', 'SCPAS_mininvite',
                 'SCPAS_mininvite_cluster', 'SCPAS_minnetsucc', 'SCPAS_minnetsucc_cluster', 'UCCminsucc',
                 'UCCminsucc_cluster']
    cl_items = ['2gcl_minsucc', '2gcl_minsucc_cluster', 'CLAS_minnetsucc', 'CLAS_minnetsucc_cluster',
                'CLAS_minplaysucc', 'CLAS_minplaysucc_cluster', 'CLAS_mininvite', 'CLAS_mininvite_cluster',
                'VRBT_minplaysucc', 'VRBT_minplaysucc_cluster', 'videobandwidth_ratio', 'videobandwidth_ratio_cluster',
                'videoplay_ratio', 'videoplay_ratio_cluster']
    # 查询scp相关业务指标
    scp_data = query_zb(scp_items, date)
    # 查询彩铃相关指标
    cl_data = query_zb(cl_items, date)
    # 获取前一天数据，计算同比
    b_scp_data = query_zb(scp_items, before_date)
    b_cl_data = query_zb(cl_items, before_date)

    # 计算同比函数
    def compare(data: dict, b_data: dict):
        # 深拷贝，避免后续迭代scp_result计算同比，同时对scp_result插入同比结果出错
        _result = dict.copy(data)
        for key, value in data.items():
            if key.endswith('cluster'):
                continue
            # 前一天的数据
            b_value = b_data.get(key, '')
            # 前一天的指标不为0，前不为空
            if value and b_value and b_value != 0:
                per = format((float(value) - float(b_value))/float(b_value), '.2%')
                # per = 'test'
            else:
                per = '-'
            _result[key + '_per'] = per
        return _result

    scp_dict = compare(scp_data, b_scp_data)
    cl_dict = compare(cl_data, b_cl_data)
    return render_template('tongji_sdata.html', app='统计数据', action="关键业务指标", date=date,
                           scp_dict=scp_dict, cl_dict=cl_dict)


@tongji.route('/pfmc')
@login_required
def performance():
    date = request.args.get('date', '')
    if not date:
        date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    engine = create_engine(current_app.config['SQLALCHEMY_BINDS']['tongji'])
    cpu_sql = "select cluste, max_cpu, max_cpu_host from as_pfmc where date={}"
    mem_sql = "select cluste, max_mem, max_mem_host from as_pfmc where date={}"
    io_sql = "select cluste, max_io, max_io_host from as_pfmc where date={}"
    cpu_data = db.session.execute(cpu_sql.format(date, date), bind=engine).fetchall()
    mem_data = db.session.execute(mem_sql.format(date, date), bind=engine).fetchall()
    io_data = db.session.execute(io_sql.format(date, date), bind=engine).fetchall()
    return render_template('tongji_pfmc.html', app='统计数据', action="主机性能数据",
                           cpu_data=cpu_data, mem_data=mem_data, io_data=io_data, date=date)


@tongji.route('/users')
@login_required
def users():
    return render_template('tongji_users.html', app='统计数据', action="用户数")
