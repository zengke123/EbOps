from . import assets
from .. import db
from ..models import Host
from sqlalchemy import distinct
from flask import jsonify, render_template, request
from flask_login import login_required


@assets.route("/info/<hostname>", methods=['GET', 'POST'])
@login_required
def get_host_info(hostname):
    host = Host.query.filter(Host.hostname == hostname).first()
    return render_template('assets_info.html', app="资产管理", action="资产详情", host=host)


@assets.route("/update/<hostname>", methods=['GET', 'POST'])
@login_required
def update_host_info(hostname):
    if request.method == "GET":
        host_info = Host.query.filter(Host.hostname == hostname).first()
        return render_template('assets_update.html', app="资产管理", action="资产更新", host=host_info)
    elif request.method == "POST":
        m_host = request.form
        try:
            db.session.query(Host).filter(Host.hostname == hostname).update(m_host)
            db.session.commit()
            return "success"
        except Exception as e:
            print(str(e))
            return "fail"