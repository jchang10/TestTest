from flask import request, url_for
from flask_restful import Api, Resource, reqparse, fields, marshal, abort

from myapp.auth import httpauth
from myapp.models import db, User
from ..decorators import json, collection, etag


user_fields = {
    'email': fields.String,
    'username': fields.String,
    'uri': fields.Url('api.user', absolute=True),
    'password_hash': fields.String
}


class UserListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, location='json')
        self.reqparse.add_argument('username', type=str, default="", location='json',
                                   required=True,
                                   help='username is required. can be same as email.'
        )
        self.reqparse.add_argument('password', type=str, location='json')
        super(UserListAPI, self).__init__()

    def get(self):
        return {'users': [marshal(user, user_fields) for user in User.query]}

    def post(self):
        args = self.reqparse.parse_args()
        if User.query.filter_by(username=args['username']).first() is not None:
            abort(400, message="Username already exists.")
        if User.query.filter_by(email=args['email']).first() is not None:
            abort(400, message="Email already exists.")
        user = User(email=args['email'],
                    username=args['username'] if args['username'] else args['email'])
        if args['password']:
            user.password = args['password']
        db.session.add(user)
        db.session.commit()
        return {'user': marshal(user, user_fields)}, 201, \
               {'Location': url_for('api.user', id=user.id)}
    

class UserAPI(Resource):
    decorators = [httpauth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, location='json')
        self.reqparse.add_argument('username', type=str, location='json')
        super(UserAPI, self).__init__()
        
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User with given id was not found.")
        return {'user': marshal(user, user_fields)}

    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User with given id was not found.")
        db.session.delete(user)
        db.session.commit()
        return {'result': True}
    
