
import boto3, os

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    socials = db.relationship('OauthUser', backref='user',
                                lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        if self.password_hash:
            return check_password_hash(self.password_hash, password)
        return False

    def __repr__(self):
        return '<User %r>' % self.username

    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user


class OauthUser(db.Model):
    __tablename__ = 'oauth_users'
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(64), nullable=False)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    username = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    name = db.Column(db.String(64), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    
class MyData(db.Model):
    __tablename__ = 'mydata'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64))
    date = db.Column(db.String(20))
    score = db.Column(db.Integer)
    weighting = db.Column(db.Float)

    def __repr__(self):
        return '<MyData %r>' % self.name

    def to_json(self):
        mydata = {
            'customer_id':self.customer_id,
            'name':self.name,
            'date':self.date,
            'score':self.score,
            'weighting':self.weighting
            }
        return mydata

    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
