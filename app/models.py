from datetime import datetime
from app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.sql import func


class Citizen(db.Model, UserMixin):
    citizen_id = db.Column(db.String(12), primary_key=True)
    name = db.Column(db.String(64), index=True)
    eval_complete = db.Column(db.Integer)
    score = db.Column(db.Float)
    password_hash = db.Column(db.String(128))
    permission = db.Column(db.String(20), index=True, default='citizen')
    profile_image = db.Column(db.String(100))
    bio = db.Column(db.String(200))
    fav_leader = db.Column(db.String(30))
    income = db.Column(db.Integer)

    def __repr__(self):
        return '<Citizen {}>'.format(self.citizen_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return (self.citizen_id)

    def set_pic(self, url):
        if url:
            self.profile_image = url


@login.user_loader
def get_user(citizen_id):
    return Citizen.query.get(citizen_id)


class Report(db.Model):
    reporter_id = db.Column(db.String(12), db.ForeignKey('citizen.citizen_id'))
    reported_id = db.Column(db.String(12), db.ForeignKey('citizen.citizen_id'))
    report_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    report_category = db.Column(db.String(64), default='betrayal')
    body = db.Column(db.String(140))

    def __repr__(self):
        return '<Report {}>'.format(self.body)


class Status(db.Model):
    citizen_id = db.Column(db.String(12), db.ForeignKey('citizen.citizen_id'))
    status_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status_category = db.Column(db.String(64), default='self-praise')
    body = body = db.Column(db.String(140))

    def __repr__(self):
        return '<Status {}>'.format(self.body)


class Image(db.Model):
    image_id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(100))

    def __repr__(self):
        return '<Image {}>'.format(self.body)

    def get_rand(self):
        return random.choice(self.query.all())
