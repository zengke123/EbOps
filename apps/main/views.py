from . import main
from .. import db
from ..models import OpsItem
from flask import render_template
from flask_login import login_required


@main.route("/",methods=['GET','POST'])
@login_required
def index():
    ops_items = db.session.query(OpsItem.t_name, OpsItem.c_name).all()
    return render_template('index.html', ops_items=ops_items)