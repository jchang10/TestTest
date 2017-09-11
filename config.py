
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': '1815640065363616',
            'secret': '132dfefaf3eaf315c0708ed5a39d559f'
        },
        'twitter': {
            'id': 'LhJtMKjn5NcBRwwfT9oDC60ew',
            'secret': '1bpwiwh3XaVDvtBgOA5ve8U9i5VCN6qvNG0vYDHxPZ5Pts25mz'
        },
        'google': {
            'id': '583774673754-h61i7a1ljrp4in0o3fb90p7kste7m3vu.apps.googleusercontent.com',
            'secret': '7X2z6H6zg5RFDFWXTFVEDgU_'
        },
    }

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')
                              
class AWSTestingConfig(Config):
    DEBUG = False
    TEST = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or None

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI') or None
    
config = {
    'dev': DevelopmentConfig,
    'testing': TestingConfig,
    'awstest': AWSTestingConfig,
    'prod': ProductionConfig,
    'default': DevelopmentConfig
}
