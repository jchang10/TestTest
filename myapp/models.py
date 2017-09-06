
import boto3
import os

from flask_sqlalchemy import SQLAlchemy

from . import db

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

