from . import check
from .. import db
from ..models import CheckHost, Host
from sqlalchemy import distinct
from flask import jsonify, request
from flask_login import login_required


@check.route("/get_nodes", methods=['GET', 'POST'])
@login_required
def get_nodes():
    cluste_type = db.session.query(distinct(CheckHost.node)).all()
    nodes = [x[0] for x in cluste_type]
    # ztree 一级节点
    z_nodes = []
    for i, node in enumerate(nodes):
        cluste_temps = db.session.query(distinct(CheckHost.cluster)).filter(CheckHost.node == node).order_by(
            CheckHost.cluster).all()
        clusters = [x[0] for x in cluste_temps]
        # 二级节点
        childrens = [{'name': cluster} for cluster in clusters]
        p1_data = {
            'name': node + " ({})".format(len(clusters)),
            'open': 'true' if i == 0 else 'false',
            'children': childrens
        }
        z_nodes.append(p1_data)
    return jsonify(z_nodes)


@check.route("/get_hosts", methods=['GET', 'POST'])
def get_hosts():
    cluester = request.form.get('cluster')
    hosts_temp = CheckHost.query.filter(CheckHost.cluster == cluester).all()
    hosts = [x.hostname for x in hosts_temp]
    result = []
    host_ip = None
    for i, x in enumerate(hosts):
        try:
            ip = db.session.query(Host.local_ip).filter(Host.hostname == x).one()
            host_ip = ip[0]
        except Exception as e:
            host_ip = ""
        finally:
            result.append({
                'id': i,
                'name': x,
                'ip': host_ip
            })
    # result = [{'id': i, 'name': x.hostname} for i, x in enumerate(hosts_temp)]
    return jsonify(result)
