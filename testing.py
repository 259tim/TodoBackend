import os

from flask.wrappers import Response
from app import app, db
import unittest

TEST_DB = 'test.db'

class BasicTestCase(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()


    def test_landing(self):
        result = self.app.get('/')
        
        self.assertEqual(result.status_code, 200)
