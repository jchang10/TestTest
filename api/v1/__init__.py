from flask import Blueprint, g, url_for, jsonify
from flask_restful import Api, Resource

from ..errors import ValidationError, bad_request, not_found
#from ..auth import auth
from ..decorators import json, rate_limit

from .users import UserListAPI, UserAPI

api = Blueprint('api', __name__)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class AppCatalogAPI(Resource):
    def get(self):
        return {
            'users_url': url_for('api.users', _external=True)
        }

    
rest_api = Api(api, prefix="/v1")
rest_api.add_resource(HelloWorld, "/helloworld")
rest_api.add_resource(AppCatalogAPI, "/")
rest_api.add_resource(UserListAPI, "/users", endpoint='users')
rest_api.add_resource(UserAPI, "/user/<int:id>", endpoint='user')    


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(str(e))


@api.errorhandler(400)
def bad_request_error(e):
    return bad_request('invalid request')


@api.before_request
#@auth.login_required
@rate_limit(limit=5, period=15)
def before_request():
    pass


@api.after_request
def after_request(response):
    if hasattr(g, 'headers'):
        response.headers.extend(g.headers)
    return response

