import time
from flask import Flask, request, abort, jsonify, url_for
from models.user import db, login, User

# https://blog.miguelgrinberg.com/post/restful-authentication-with-flask
# because the app is accessed through Expo/React Native
# you have to host the application on your public network
# the localhost does NOT work.
# in app.run I put: host=192.168.178.11" <- check your local device IP
#  this depends on your situation, and change accordingly
# 'ipconfig' on Windows or `ip address`/`ifconfig` on Linux to check

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quickscan.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


login.init_app(app)


# app.run(host='192.168.178.11', port=5000)

@app.route('/time', methods=['GET'])
def get_current_time():
    return {'time': User.query.count()}


@app.route('/api/users', methods=['POST'])
def new_user():
    myRequest = request.get_json('email')
    email = myRequest.get('email')
    password = myRequest.get('password')
    name = myRequest.get('name')
    print("hello:")
    print(email)

    if email is None or password is None:
        print("abort1")
        abort(400)  # missing arguments!

    if User.query.filter_by(email=email).first() is not None:
        print("abort2")
        abort(400)  # user exists

    print("here")
    user = User(email=email, name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'name': user.name})  #, 201, {'Location': url_for('get_user', id=user.id, _external=True)}
