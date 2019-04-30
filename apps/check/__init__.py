from flask import Blueprint

check = Blueprint('check', __name__)

from . import views