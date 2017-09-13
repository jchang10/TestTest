from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    
    # apply configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # initialize extensions
    db.init_app(app)

    # register blueprints
    from api.v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")
    
    return app

