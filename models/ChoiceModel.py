from app import db, ma
from models.QuestionModel import Question

# obsolete for now, see question_and_choice_model
# https://marshmallow.readthedocs.io/en/stable/examples.html

class Choice(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True)
    choice_text = db.Column(db.String())
    question_id = db.Column(db.ForeignKey('questions.id'))
    question = db.relationship("Question", backref="choices")


class ChoiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Choice

choice_schema = ChoiceSchema()
choices_schema = ChoiceSchema(many=True)
