import os
from api import app
import pytest
import tempfile
from flask_sqlalchemy import SQLAlchemy
from dbcreation import create_test_db
import json

@pytest.fixture
def client():
    # have tempfile as test database, and set the app to test mode
    test_db, app.config['DATABASE'] =tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            # create the temporary database
            app.config['SECRET_KEY'] = 'this key should be secure and replaced in production'
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quickscan.db'
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

            db = SQLAlchemy()
            db.init_app(app)

        yield client
    
    # close connection and unlink app from temporary database
    os.close(test_db)
    os.unlink(app.config['DATABASE'])


# tests whether landing page works
def test_landing_page(client):
        response = client.get('/')
        assert b"you are on the landing page" in response.data

# test whether we can POST to the database
def test_posting_user(client):

    data = {
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

# test whether we can GET from the database
def test_getting_participations(client):

    data = {
        'email': 'testuser@test.com',
        'name': 'Tim Tester',
        'password': 'password'
    }

    response = client.get('/api/participations', 
    data=json.dumps(data),
     follow_redirects = True
     )

    print(response.data)
    assert {
        'id': '1',
        'survey_name':'Quick Scan Test Survey'
    } in response.data

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