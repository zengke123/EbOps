from flask import Blueprint

operation = Blueprint('operation', __name__)

from . import views