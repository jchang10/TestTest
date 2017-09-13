from flask import Blueprint
from flask_httpauth import HTTPBasicAuth

auth = Blueprint('auth', __name__)
httpauth = HTTPBasicAuth()

from . import views
