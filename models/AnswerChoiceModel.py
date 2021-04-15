from app import db, ma


class AnswerChoice(db.Model):
    __tablename__ = 'answer_choices'

    answer_key = db.Column(db.ForeignKey('answers.id'), primary_key=True)
    choice_key = db.Column(db.ForeignKey('choices.id'), primary_key=True)


class AnswerChoiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AnswerChoice
