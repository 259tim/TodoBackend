from app import db, ma

answer_choice_association = db.Table(
    'answer_choice_association',
    db.metadata,
    db.Column('answer_id', db.Integer, db.ForeignKey('answers.id')),
    db.Column('choice_id', db.Integer, db.ForeignKey('choices.id'))
    )

class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    participation_key = db.Column(db.ForeignKey('participations.id'))
    question_key = db.Column(db.ForeignKey('questions.id'))
    open_answer = db.Column(db.String())
    bool_answer = db.Column(db.Boolean())
    choices = db.relationship('Choice',
    secondary= answer_choice_association)


class AnswerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Answer


answer_schema = AnswerSchema()
answers_schema = AnswerSchema(many=True)
