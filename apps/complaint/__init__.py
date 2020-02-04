from flask import Blueprint

complaint = Blueprint('complaint', __name__)

from . import views