from flask import Blueprint

operate = Blueprint('operate', __name__)

from . import views