import datetime
from . import tongji
from .. import db
from flask import render_template, current_app, request
from flask_login import login_required
from sqlalchemy import create_engine


@tongji.route('/data')
@login_required
def profiledata():
    return render_template('tongji_sdata.html', app='统计数据', action="关键业务指标")


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


@tongji.route('/ops')
@login_required
def ops():
    return render_template('tongji_ops.html', app='统计数据', action="作业计划指标")
