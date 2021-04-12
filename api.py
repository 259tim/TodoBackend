from flask_httpauth import HTTPBasicAuth
from flask import request, jsonify, g
# from models.AnswerChoiceModel import AnswerChoice
# from models.AnswerModel import Answer
# from models.ChoiceModel import Choice
# from models.ParticipationModel import Participation
# from models.surveyModel import Survey
# from models.SurveyQuestionModel import SurveyQuestion
from models.userModel import User
from app import app
import time
from db import db, login

# https://blog.miguelgrinberg.com/post/restful-authentication-with-flask
# https://medium.com/@stevenrmonaghan/password-reset-with-flask-mail-protocol-ddcdfc190968
# because the app is accessed through Expo/React Native
# you have to host the application on your public network
# the localhost does NOT work.
# in app.run I put: host=192.168.178.11" <- check your local device IP
# you can also do 'flask run --host IPHERE'
#  this depends on your situation, and change accordingly
# 'ipconfig' on Windows or `ip address`/`ifconfig` on Linux to check
# to run this app you have to activate the virtual environment with 'source venv/bin/activate'


app.config['SECRET_KEY'] = 'this key should be secure and replaced in production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quickscan.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

auth = HTTPBasicAuth()
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


login.init_app(app)


# app.run(host='192.168.178.11', port=5000)

@auth.verify_password
def verify_password(email_or_token, password):
    # first try to authenticate by token

    user = User.verify_auth_token(email_or_token)
    if not user:
        # try to authenticate with email/password
        user = User.query.filter_by(email = email_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@auth.error_handler
def unauthorized():
    response = jsonify({'message':'Failed'})
    return response


@app.route('/time', methods=['GET'])
def get_current_time():
    return {'time': time.time()}


@app.route('/api/usercreate', methods=['POST'])
def new_user():
    myRequest = request.get_json('email')
    email = myRequest.get('email')
    password = myRequest.get('password')
    name = myRequest.get('name')

    if email == "" or password == "" or name == "" or email is None or password is None or name is None:
        print("abort_missing")
        return jsonify(message= "Missing arguments")  # missing arguments!

    if User.query.filter_by(email=email).first() is not None:
        print("abort_exists")
        return jsonify(message= "User exists")  # user exists

    user = User(email=email, name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'name': user.name})  #, 201, {'Location': url_for('get_user', id=user.id, _external=True)}

# curl -u user:pw -i -X GET http://192.168.178.11:5000/api/lockedaway
# https://curl.trillworks.com/
# this is password auth. Token auth is preferred.


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(10)
    return jsonify({'token': token.decode('ascii'), 'duration': 120})

# this is an example of a page that requires verification to enter
# the login_required refers back to the authentication library and calls the relevant
# functions that were made in the user model.
@app.route('/api/lockedaway')
@auth.login_required
def get_lockedaway():
    return jsonify({'data': 'Hello, %s! this is secret!' % g.user.name})
