import os
from api import app, db
import pytest
import tempfile
from flask_sqlalchemy import SQLAlchemy
from dbcreation import create_test_db
import json

@pytest.fixture
def client():
    db, app.config['DATABASE'] =tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            app.config['SECRET_KEY'] = 'this key should be secure and replaced in production'
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quickscan.db'
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

            db = SQLAlchemy()
            db.init_app(app)
            create_test_db()

        yield client
    
    os.close(db)
    os.unlink(app.config['DATABASE'])


def test_landing_page(client):
        response = client.get('/')
        assert b"you are on the landing page" in response.data


def test_posting_user(client):

    data={
        'email': 'testuser@test.com',
        'name': 'Tim Tester',
        'password': 'password'
    }

    response = client.post('/api/usercreate', 
    data=json.dumps(data),
     follow_redirects = True
     )

    print(response.data)
    assert b' "name": "Tim Tester"\n' in response.data




# def login(client, username, password):
#     return client.post('/login', data=dict(
#         username=username,
#         password=password
#     ), follow_redirects=True)


# def test_login(client):
#     username = app.config["username"]
#     password = app.config["password"]

#     response = client.get('a')
#     assert 