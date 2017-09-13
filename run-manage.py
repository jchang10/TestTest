import os

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from myapp import create_app, db
from myapp.models import User, Role


myapp = create_app(os.getenv('STAGE') or 'default')
manager = Manager(myapp)
migrate = Migrate(myapp, db)


def make_shell_context():
    return dict(myapp=myapp, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

    
if __name__ == '__main__':
    manager.run()
