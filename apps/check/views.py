from . import check
from flask import render_template, request, jsonify
from flask_login import login_required



@check.route("/info", methods=['GET','POST'])
@login_required
def info():
    return render_template('check_list.html', app="自动例检", action="主机例检")