from . import check
from .. import db
from ..models import CheckHost
from sqlalchemy import distinct
from flask import jsonify
from flask_login import login_required


@check.route("/get_nodes", methods=['GET','POST'])
@login_required
def get_nodes():
    cluste_type = db.session.query(distinct(CheckHost.node)).all()
    nodes = [x[0] for x in cluste_type]
    # ztree 一级节点
    zNodes = []
    for i, node in enumerate(nodes):
        cluste_temps = db.session.query(distinct(CheckHost.cluster)).filter(CheckHost.node == node).order_by(
            CheckHost.cluster).all()
        clusters = [x[0] for x in cluste_temps]
        # 二级节点
        childrens = [{'name': cluster} for cluster in clusters]
        p1_data = {
            'name': node + " ({})".format(len(clusters)),
            'open': 'true' if i==0 else 'false',
            'children': childrens
        }
        zNodes.append(p1_data)
    return jsonify(zNodes)