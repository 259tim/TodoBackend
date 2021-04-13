from app import db


class Choice(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True)
    question_key = db.Column(db.ForeignKey('questions.id'))
    choice_text = db.Column(db.String())
