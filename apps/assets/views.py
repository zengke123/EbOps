from . import assets
from .. import db
from ..models import Host
from sqlalchemy import distinct
from flask import jsonify, render_template
from flask_login import login_required


@assets.route("/info/<hostname>", methods=['GET','POST'])
@login_required
def get_host_info(hostname):
    host = Host.query.filter(Host.hostname == hostname).first()
    return render_template('assets_info.html', app="资产管理", action="资产详情", host=host)


@assets.route("/update/<hostname>", methods=['GET','POST'])
@login_required
def update_host_info(hostname):
    return render_template('assets_update.html', app="资产管理", action="资产更新")