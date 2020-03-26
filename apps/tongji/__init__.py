from flask import Blueprint

tongji = Blueprint('tongji', __name__)

from . import views, apis
