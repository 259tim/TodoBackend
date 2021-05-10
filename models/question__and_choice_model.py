from app import db, ma
from marshmallow_sqlalchemy.fields import Nested

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String())
    # there are four types:
    # 0: yes/no: boolean
    # 1: multiple choice,single answer (radio buttons)
    # 2: multiple choice, multiple answers (check boxes)
    # 3: open answer: string
    question_type = db.Column(db.Integer())

class Choice(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True)
    choice_text = db.Column(db.String())
    question_id = db.Column(db.ForeignKey('questions.id'))
    question = db.relationship("Question", backref="choices")


class ChoiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Choice


class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Question
    id = ma.auto_field()
    question_text = ma.auto_field()
    question_type = ma.auto_field()
    choices = Nested(ChoiceSchema, many=True)


question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)
choice_schema = ChoiceSchema()
choices_schema = ChoiceSchema(many=True)
