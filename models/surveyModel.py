from app import db, ma


class Survey(db.Model):
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)
    survey_name = db.Column(db.String(128))


class SurveySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Survey
