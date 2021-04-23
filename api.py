from flask_httpauth import HTTPBasicAuth
from flask import request, jsonify, g
from flask_login import LoginManager
from models.AnswerChoiceModel import AnswerChoice
from models.AnswerModel import Answer, answer_schema, answers_schema
from models.ChoiceModel import Choice
from models.ParticipationModel import Participation, participation_schema, participations_schema
from models.QuestionModel import Question, question_schema, questions_schema
from models.surveyModel import Survey, survey_schema, surveys_schema
from models.SurveyQuestionModel import SurveyQuestion
from models.userModel import User
from app import app, db


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


auth = HTTPBasicAuth()
login = LoginManager()


# initialize login checker
login.init_app(app)

# Initialize the app and database:
# This makes sure the database system understands the flask app.
# It also adds a set of data to test with.

with app.app_context():

    db.create_all()

    # add test user
    if User.query.filter_by(email="tim.seip@capgemini.com").first() is not None:
        print("test user exists, not creating test dataset")
    else:
        print("inserting test datasetc")
        user = User(email="tim.seip@capgemini.com", name="admin")
        user.set_password("adminpw")
        db.session.add(user)

        # add test survey
        survey = Survey(survey_name="cookie survey")

        db.session.add(survey)

        # add test questions
        TQ1 = Question(question_type=0, question_text="Do you like cookies?")  # yes/no
        TQ2 = Question(question_type=1, question_text="Choose your favourite flavour.")  # multiple choice one answer
        TQ3 = Question(question_type=2, question_text="Choose all types of cookies that you enjoy.")  # multiple choice multiple answer
        TQ4 = Question(question_type=3, question_text="Please describe how cookies make you feel.")  # open

        db.session.add(TQ1)
        db.session.add(TQ2)
        db.session.add(TQ3)
        db.session.add(TQ4)

        # link test questions to test survey
        SQ1 = SurveyQuestion(question_id=1, survey_id=1, category_weight_one=1,
        category_weight_two=2, category_weight_three=3, category_weight_four=4, category_weight_five=5)
        SQ2 = SurveyQuestion(question_id=2, survey_id=1, category_weight_one=1,
        category_weight_two=2, category_weight_three=3, category_weight_four=4, category_weight_five=5)
        SQ3 = SurveyQuestion(question_id=3, survey_id=1, category_weight_one=1,
        category_weight_two=2, category_weight_three=3, category_weight_four=4, category_weight_five=5)
        SQ4 = SurveyQuestion(question_id=4, survey_id=1, category_weight_one=1,
        category_weight_two=2, category_weight_three=3, category_weight_four=4, category_weight_five=5)
        SQ5 = SurveyQuestion(question_id=5, survey_id=1, category_weight_one=1,
        category_weight_two=2, category_weight_three=3, category_weight_four=4, category_weight_five=5)

        db.session.add(SQ1)
        db.session.add(SQ2)
        db.session.add(SQ3)
        db.session.add(SQ4)
        db.session.add(SQ5)

        # give the multiple choice questions possible choices
        C1 = Choice(question_id=2, choice_text="strawberry.")
        C2 = Choice(question_id=2, choice_text="apple.")
        C3 = Choice(question_id=2, choice_text="custard.")
        C4 = Choice(question_id=3, choice_text="soft cookies.")
        C5 = Choice(question_id=3, choice_text="hard cookies.")
        C6 = Choice(question_id=3, choice_text="chocolate cookies.")
        C7 = Choice(question_id=3, choice_text="british biscuits.")
        C8 = Choice(question_id=3, choice_text="american chocolate chip.")
        C9 = Choice(question_id=3, choice_text="cookies for tea.")
        C10 = Choice(question_id=3, choice_text="cookies for coffee.")
        C11 = Choice(question_id=3, choice_text="cookies for hot chocolate.")
        C12 = Choice(question_id=3, choice_text="cookies for dessert.")

        db.session.add(C1)
        db.session.add(C2)
        db.session.add(C3)
        db.session.add(C4)
        db.session.add(C5)
        db.session.add(C6)
        db.session.add(C7)
        db.session.add(C8)
        db.session.add(C9)
        db.session.add(C10)
        db.session.add(C11)
        db.session.add(C12)

        # commit all this to the DB
        db.session.commit()
        print("test dataset added")

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


# these are the API's routes, first we initialize the API


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
    return jsonify({'message': "participation with key '%s' has been added" % new_participation.reference_key})

# question API section

# get all questions
@app.route('/api/questions')
@auth.login_required
def questions():
    all_questions = Question.query.all()
    return questions_schema.jsonify(all_questions)


# get a specific survey
@app.route("/api/questions/<id>", methods = ["GET"])
@auth.login_required
def question_detail(id):
    survey = Survey.query.get(id)
    return survey_schema.dump(survey)
