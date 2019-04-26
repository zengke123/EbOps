from flask import Blueprint

ops = Blueprint('ops', __name__)

from . import views