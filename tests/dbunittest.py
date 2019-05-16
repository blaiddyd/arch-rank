import unittest, os
from app import app, db
from app.models import Citizen, Report, Status

def gen_id():
    chars = string.digits
    return int(''.join(random.choice(chars) for _ in range(0, 6)))

class CitizenTest(unittest.TestCase):
    def init(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI']=\
            'sqlite:///'+os.path.join(basedir,'test.db')
        self.app = app.test_client()
        db.create_all()
        a_citizen = Citizen(citizen_id='12345678', name='An Average Joe', score=80, permission='citizen')
        another_citizen = Citizen(citizen_id='09876543', name='God Tier', score=10000000, permission='citizen')
        report = Report(reporter_id=another_citizen.citizen_id, reported_id=a_citizen.citizen_id, report_id=gen_id(), body="A peasant and nothing more")
        status = Status(citizen_id=a_citizen, status_id=gen_id(), body="I'm just a great man!")
        db.session.add(a_citizen)
        db.session.add(another_citizen)
        db.session.add(report)
        db.session.add(status)
        db.session.commit()

    def password_test(self):
        citizen = Citizen.query.get('12345678')
        citizen.set_password('loser')
        self.assertFalse(citizen.check_password('winner'))
        self.assertTrue(citizen.check_password('loser'))
        
