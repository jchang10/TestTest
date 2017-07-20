
import os
import csv
from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

basedir = os.path.abspath(os.path.dirname(''))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

db = SQLAlchemy(app)
db.create_all()

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

@app.route("/")
def index():
    if MyData.query.count():
        return render_template('query.html')
    else:
        return redirect(url_for('uploader'))

@app.route("/upload", methods = ['GET','POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        count = add_db_records(f.filename)
        str = "<h3>Successfully uploaded file with %d records</h3>" % (count)
        return str + render_template('query.html')
    else:
        return render_template('upload.html')

@app.route("/view")
def view():
    if request.args.get('upload'):
        return redirect(url_for('uploader'))
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

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0')
    

