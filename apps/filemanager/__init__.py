from flask import Blueprint

file_manager = Blueprint('file_manager', __name__)

from . import views