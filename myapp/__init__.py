
import csv
import dateutil
import os
import uuid

from flask import Flask, render_template, request, jsonify, url_for, redirect, Blueprint
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from config import config

BASEDIR = '/tmp'

db = SQLAlchemy()
bootstrap = Bootstrap()
myapp = Blueprint('myapp', __name__)

def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)

    # apply configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # initialize extensions
    db.init_app(app)
    bootstrap.init_app(app)

    # register blueprints
    app.register_blueprint(myapp)

    return app

from .models import MyData

@myapp.route("/testme")
def testme():
    return "The URL for this page is {}".format(url_for('myapp.testme'))

@myapp.route("/")
def index():
    if MyData.query.count():
        return render_template('query.html')
    else:
        return redirect(url_for('myapp.uploader'))

@myapp.route("/upload", methods = ['GET','POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(BASEDIR, f.filename))
        count = add_db_records(os.path.join(BASEDIR, f.filename))
        str = "<h3>Successfully uploaded file with %d records</h3>" % (count)
        return str + render_template('query.html')
    else: # GET
        return render_template('upload.html')

@myapp.route("/view")
def view():
    if request.args.get('upload'):
        return redirect(url_for('myapp.uploader'))

    headers = ["id","customer_id","name","score","weighting"]
    rows = None
    filter = request.args.get('filter', type=str)
    if filter:
        rows = MyData.query.filter(text(filter)).all()
    else:
        rows = MyData.query.all()

    if request.args.get('json'):
        return jsonify([r.to_json() for r in rows])
    else:
        return render_template('view.html', headers=headers, rows=rows, filter=filter)
    
def add_db_records(filename):
    data = []
    with open(filename) as f:
        r = csv.reader(f)
        headers = next(r)
        for row in r:
            d = MyData(**dict(zip(headers,row)))
            data.append(d)
    db.session.add_all(data)
    db.session.commit()
    return len(data)

@myapp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


