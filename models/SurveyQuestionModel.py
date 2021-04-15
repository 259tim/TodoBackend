from app import db, ma


class SurveyQuestion(db.Model):
    __tablename__ = 'survey_questions'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'))
    category_weight_one = db.Column(db.Integer)
    category_weight_two = db.Column(db.Integer)
    category_weight_three = db.Column(db.Integer)
    category_weight_four = db.Column(db.Integer)
    category_weight_five = db.Column(db.Integer)


class SurveyQuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SurveyQuestion
