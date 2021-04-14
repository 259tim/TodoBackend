from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SECRET_KEY'] = 'this key should be secure and replaced in production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quickscan.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)


ma = Marshmallow(app)
