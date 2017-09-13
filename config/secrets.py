
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Secrets:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI')
                              
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

class DevelopmentSecrets(Secrets):
    SQLALCHEMY_DATABASE_URI = \
      'postgresql://imvutest:blahblah@imvutest.cix6ebfre1yf.us-west-1.rds.amazonaws.com/imvutestdb'
    
class TestingSecrets(Secrets):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or None
    
class AWSTestingSecrets(Secrets):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or None

class ProductionSecrets(Secrets):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI') or None
    
secrets = {
    'dev': DevelopmentSecrets,
    'testing': TestingSecrets,
    'awstest': AWSTestingSecrets,
    'prod': ProductionSecrets,
    'default': DevelopmentSecrets
}

