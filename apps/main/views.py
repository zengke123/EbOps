from . import main
from .. import db
from flask import render_template, current_app
from flask_login import login_required
from sqlalchemy import create_engine


@main.route("/", methods=['GET', 'POST'])
@login_required
def index():
    import datetime
    # 创建engine 连接tongji库
    engine = create_engine(current_app.config['SQLALCHEMY_BINDS']['tongji'])
    # 查询近两天的用户数
    user_datas = db.session.execute("select vpmn_volte,hjh_volte,pyq_volte,vh_volte,vp_volte,hp_volte,vhp_volte, crbt_volte,vrbt,ctx_group,ctx_user from users order by date desc limit 2",
                                    bind=engine).fetchall()

    # 数据验证
    def validate(x):
        if x:
            try:
                x = int(x)
                return x
            except ValueError:
                return 0
        else:
            return 0

    # 计算同比
    def compare(_x, _y):
        if _y != 0:
            _result = format((_x - _y)/_y, '.2%')
        else:
            _result = 0
        _flag = 1 if (_x - _y) >= 0 else 0
        return _result, _flag
    # 当天用户数
    *t_vpmn_volte, t_crbt, t_vrbt, t_ctx_g, t_ctx_u = [validate(x) for x in user_datas[0]]
    # Volte智能网总用户数
    t_v_users = sum(t_vpmn_volte)
    # ctx总用户数
    t_ctx_users = t_ctx_g + t_ctx_u
    # 前一天用户数
    *y_vpmn_volte, y_crbt, y_vrbt, y_ctx_g, y_ctx_u = [validate(x) for x in user_datas[1]]
    # 前一天Volte智能网总用户数
    y_v_users = sum(y_vpmn_volte)
    # 前一天ctx总用户数
    y_ctx_users = y_ctx_g + y_ctx_u
    # 计算同比
    vpmn_per, vpmn_per_flag = compare(t_v_users, y_v_users)
    crbt_per, crbt_per_flag = compare(t_crbt, y_crbt)
    vrbt_per, vrbt_per_flag = compare(t_vrbt, y_vrbt)
    ctx_per, ctx_per_flag = compare(t_ctx_users, y_ctx_users)
    datas = db.session.execute("select `date`,`scpas_caps`,`catas_caps` from caps where date_sub(curdate(), INTERVAL 15 DAY) <= date(`date`);",
                               bind=engine).fetchall()
    date = [int(x[0]) for x in datas]
    scpas_caps = [x[1] for x in datas]
    catas_caps = [x[2] for x in datas]
    # 计算性能数据
    # yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    yesterday = '20180909'
    cpu_sql = "select cluste, max_cpu, max_cpu_host from as_pfmc where date={} " \
              "and max_cpu=(select max(max_cpu) from as_pfmc where date='{}')"
    mem_sql = "select cluste, max_mem, max_mem_host from as_pfmc where date={} " \
              "and max_mem=(select max(max_mem) from as_pfmc where date='{}')"
    io_sql = "select cluste, max_io, max_io_host from as_pfmc where date={} " \
              "and max_io=(select max(max_io) from as_pfmc where date='{}')"
    cpu_data = db.session.execute(cpu_sql.format(yesterday, yesterday), bind=engine).fetchall()
    mem_data = db.session.execute(mem_sql.format(yesterday, yesterday), bind=engine).fetchall()
    io_data = db.session.execute(io_sql.format(yesterday, yesterday), bind=engine).fetchall()
    return render_template('index.html', **locals())
