from app import db


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
