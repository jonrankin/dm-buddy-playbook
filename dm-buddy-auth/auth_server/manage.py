# api/manage.py

import os
import unittest
import coverage

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from pprint import pprint

COV = coverage.coverage(
    branch=True,
    include='auth/*',
    omit=[
        'auth/tests/*',
        'auth/config.py',
        'auth/*/__init__.py'
    ]
)
COV.start()

from auth import app, db
from auth.db_access import models

manager = Manager(app)

@manager.command
def test():
     """Runs unit tests without test coverage."""
     tests = unittest.TestLoader().discover('auth/tests/', pattern='test_auth.py')
     result = unittest.TextTestRunner(verbosity=2).run(tests)
     if result.wasSuccessful():
	return 0
     return 1


if __name__ == '__main__':
    manager.run()
