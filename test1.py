
import os
from myapp import create_app

app = create_app(os.environ.get('FLASK_CONFIG', 'development'))

if __name__ == '__main__':
    # with app.app_context():
    #     #db.create_all()
    #     # create a development user
    #     if User.query.get(1) is None:
    #         u = User(username='john')
    #         u.set_password('cat')
    #         db.session.add(u)
    #         db.session.commit()
    app.run(debug=True, host='0.0.0.0')
    

