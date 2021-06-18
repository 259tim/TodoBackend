from flask_httpauth import HTTPBasicAuth
from flask import request, jsonify, g
from flask_login import LoginManager
from models.question__and_choice_model import Question, question_schema, questions_schema, Choice, choice_schema, choices_schema
from models.AnswerModel import Answer, answer_schema, answers_schema
from models.ParticipationModel import Participation, participation_schema, participations_schema
from models.surveyModel import Survey, survey_schema, surveys_schema
from models.SurveyQuestionModel import SurveyQuestion
from models.userModel import User
from app import app
from dbcreation import create_test_db
import json

# to run this app you have to first activate the virtual environment with 'source venv/bin/activate'

# because the app is accessed through Expo/React Native
# you have to host the application on your public network, the localhost does NOT work.
# do 'flask run --host IPHERE' > "flask run --host 192.168.178.11" <- check your local device IP
# this depends on your situation, please change accordingly
# 'ipconfig' on Windows or `ip address`/`ifconfig` on Linux to check your LOCAL! IP address.



auth = HTTPBasicAuth()
login = LoginManager()


# initialize login checker
login.init_app(app)

@login.user_loader
def load_user(user_id):
    return User.get(id)

# add the test database:
create_test_db()


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
    response = jsonify({'message':'login failed'})
    return response


# these are the API's routes

# basic GET

@app.route('/')
def landing():
    return "you are on the landing page"


# create a new user

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
        return jsonify(message="User exists")  # user exists

    user = User(email=email, name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'name': user.name})  #, 201, {'Location': url_for('get_user', id=user.id, _external=True)}



# get authentication token
# this is an example of a page that requires verification to enter
# the login_required refers back to the authentication library and calls the relevant
# functions that were made in the user model.

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(10)
    return jsonify({'token': token.decode('ascii'), 'duration': 120})

# login route

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

# survey API section

# get all surveys
@app.route('/api/surveys')
@auth.login_required
def surveys():
    all_surveys = Survey.query.all()
    return surveys_schema.jsonify(all_surveys)


# get a specific survey
@app.route("/api/surveys/<id>", methods = ["GET"])
@auth.login_required
def survey_detail(id):

    survey = Survey.query.get(id)
    return survey_schema.dump(survey)


# participation API section

# get all participations
@app.route('/api/participations')
@auth.login_required
def participations():
    all_participations = Participation.query.all()
    return participations_schema.jsonify(all_participations)

# post a participation
@app.route("/api/participation", methods=["POST"])
@auth.login_required
def add_participation():
    req = request.get_json('reference_key')
    reference_key = req.get('reference_key')
    user_id = req.get('user_id')
    survey_id = req.get('survey_id')

    if reference_key == "" or user_id == "" or survey_id == "":
        print("abort_missing_participation")
        return jsonify(message= "Missing arguments")  # missing arguments!

    new_participation = Participation(reference_key=reference_key, user_id=user_id, survey_id=survey_id)
    db.session.add(new_participation)
    db.session.commit()
    return jsonify({'new_participation_id': "%s" % new_participation.id})

# question API section

# get all questions
@app.route('/api/questions')
@auth.login_required
def questions():
    all_questions = Question.query.all()
    return questions_schema.jsonify(all_questions)


# get a specific question
@app.route("/api/questions/<id>", methods = ["GET"])
@auth.login_required
def question_detail(id):
    survey = Survey.query.get(id)
    return survey_schema.dump(survey)

# post the set of questions and answers
@app.route('/api/question_post', methods=["POST"])
@auth.login_required
def add_question_set():
    req = request.get_json('whatever')  # get the data
    nested = req.get('questions')  # get the nested data
    dictresult = json.loads(nested)  # convert into dict

    participation_id = dictresult['participation_id'] # now we can take what we want from it
    questions = dictresult['questions'] # in this case the set of returned questions

    for question in questions:
        if question['question_type'] == 0 or question['question_type'] == 3:
            
            print("yes/no or bool question being inserted:")
            print (question['question_text'])
            
            dba = Answer(participation_key= participation_id, bool_answer=question['bool_choice'], open_answer=question['text_answer'], question_key=question['id'])
            db.session.add(dba)

        elif question['question_type'] == 1 or question['question_type'] == 2:

            print("radio button or checkbox question being inserted:")
            print (question['question_text'])
            choices = question['choices'] # the choices that the current question allows
            db.session.commit()

            # here we create the object, but do NOT add it yet
            # we do this so that we can query the right choice later. If we have the choice queried we can use that to make our many to many relationship
            # if we try to query while already having added this object it means there is an open connection to the database, and we can not query anything
            dba = Answer(participation_key= participation_id, bool_answer=question['bool_choice'],open_answer=question['text_answer'], question_key=question['id'])

            for choice in choices:
                if choice['chosen'] == 'checked':
                    # get the relevant choice
                    dbc = Choice.query.get(choice['id'])
                    # add the answer object from earlier
                    db.session.add(dba)
                    # then we append the relevant choice and Flask turns this into an entry in our many to many table
                    dba.choices.append(dbc)
 
            
    # commit everything
    db.session.commit()

    return jsonify({'message':'Succesfully inserted your results!'})
