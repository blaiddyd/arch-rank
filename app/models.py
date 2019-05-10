from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Citizen(db.Model, UserMixin):
    citizen_id = db.Column(db.String(12), primary_key=True)
    name  = db.Column(db.String(64), index=True)
    score = db.Column(db.Float)
    password_hash = db.Column(db.String(128))
    permission = db.Column(db.String(20), index=True, default='citizen')

    def __repr__(self):
        return '<Citizen {}>'.format(self.citizen_id)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return (self.citizen_id)

@login.user_loader
def get_user(citizen_id):
    return Citizen.query.get(citizen_id)

class Report(db.Model):
    reporter_id = db.Column(db.String(12), db.ForeignKey('citizen.citizen_id'))
    reported_id = db.Column(db.String(12), db.ForeignKey('citizen.citizen_id'))
    report_id  = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    report_category = db.Column(db.String(64))
    body = db.Column(db.String(140))

    def __repr__(self):
        return '<Report {}>'.format(self.body)
