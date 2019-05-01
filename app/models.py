from datetime import datetime
from app import db

class Citizen(db.Model):
    citizen_id = db.Column(db.String(12), primary_key=True)
    name  = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    permission = db.Column(db.String(20), index=True, default='citizen')

    def __repr__(self):
        return '<Citizen {}>'.format(self.citizen_id)

class Admin(db.Model):
    admin_id = db.Column(db.String(12), primary_key=True)
    name  = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    permission = db.Column(db.String(20), index=True, default='admin')

    def __repr__(self):
        return '<Admin {}>'.format(self.admin_id)

class Report(db.Model):
    reporter_id = db.Column(db.String(12), db.ForeignKey('citizen.citizen_id'))
    reported_id = db.Column(db.String(12), db.ForeignKey('citizen.citizen_id'))
    report_id  = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    report_category = db.Column(db.String(64))
    body = db.Column(db.String(140))

    def __repr__(self):
        return '<Report {}>'.format(self.body)
