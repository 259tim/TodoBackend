from app import db


class Survey(db.Model):
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)
    survey_name = db.Column(db.String(128))
