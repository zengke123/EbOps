from . import check
from ..models import CheckHistory
from flask import render_template, request
from flask_login import login_required


@check.route("/info", methods=['GET', 'POST'])
@login_required
def info():
    return render_template('check_list.html', app="自动例检", action="主机例检")


@check.route("/history", methods=['GET', 'POST'])
@login_required
def history():
    # 获取get请求传过来的页数,没有传参数，默认为1
    page = int(request.args.get('page', 1))
    date = request.args.get('date')
    if date:
        paginate = CheckHistory.query.filter(CheckHistory.checktime.like(date+'%')).order_by(CheckHistory.id.asc()).paginate(page, per_page=10, error_out=False)
    else:
        paginate = CheckHistory.query.order_by(CheckHistory.id.asc()).paginate(page, per_page=10, error_out=False)
    datas = paginate.items
    return render_template('check_history.html', app="自动例检", action="例检记录", paginate=paginate, datas=datas, date=date)
