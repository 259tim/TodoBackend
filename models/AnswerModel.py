from app import db


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    participation_key = db.Column(db.ForeignKey('participations.id'))
    question_key = db.Column(db.ForeignKey('questions.id'))
    open_answer = db.Column(db.String())
    bool_answer = db.Column(db.Boolean())
