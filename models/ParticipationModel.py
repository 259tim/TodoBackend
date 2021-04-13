from app import db, func


class Participation(db.Model):
    __tablename__ = 'participations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'))
    reference_key = db.Column(db.String(128))
    created_date = db.Column(db.DateTime(timezone=False), server_default=func.now())
    finished_date = db.Column(db.DateTime(timezone=False))
