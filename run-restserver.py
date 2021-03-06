import os, sys
from api.myapp import create_app

"""
python3 run-server.py
"""

app = create_app(os.environ.get('STAGE', 'default'))

if __name__ == '__main__':
    # with app.app_context():
        #db.create_all()
        # # create a development user
        # if User.query.get(1) is None:
        #     u = User(username='john')
        #     u.set_password('cat')
        #     db.session.add(u)
        #     db.session.commit()
    app.run(port=5001)

