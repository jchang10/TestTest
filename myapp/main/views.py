import csv, os

from flask import render_template, request, jsonify, url_for, redirect
from sqlalchemy.sql import text

from .. import db
from . import main
from ..models import MyData

BASEDIR = '/tmp'

@main.route("/testme")
def testme():
    return "The URL for this page is {}".format(url_for('main.testme'))

@main.route("/")
def index():
    if MyData.query.count():
        return render_template('query.html')
    else:
        return redirect(url_for('main.uploader'))

@main.route("/upload", methods = ['GET','POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(BASEDIR, f.filename))
        count = add_db_records(os.path.join(BASEDIR, f.filename))
        str = "<h3>Successfully uploaded file with %d records</h3>" % (count)
        return str + render_template('query.html')
    else: # GET
        return render_template('upload.html')

@main.route("/view")
def view():
    if request.args.get('upload'):
        return redirect(url_for('main.uploader'))

    if request.args.get('delete_all'):
        MyData.query.delete()

    headers = MyData.__table__.columns._data.keys()
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

