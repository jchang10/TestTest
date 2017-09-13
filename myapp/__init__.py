from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import config
#import ipdb; ipdb.set_trace()

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)

    # apply configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # initialize extensions
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    
    # register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from api.v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app

