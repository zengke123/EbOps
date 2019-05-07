from . import assets
from .. import db
from ..models import Host
from sqlalchemy import distinct
from flask import jsonify, render_template
from flask_login import login_required


@assets.route("/host_info/<hostname>", methods=['GET','POST'])
@login_required
def get_host_info(hostname):
    host = Host.query.filter(Host.hostname == hostname).first()
    pass
