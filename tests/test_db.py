import os
import unittest
from app import app, db
from app.models import Citizen, Report, Status
from flask import Flask

TEST_DB = 'test.db'

def gen_id():
    chars = string.digits
    return int(''.join(random.choice(chars) for _ in range(0, 6)))

class Tests(unittest.TestCase):
    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

        self.assertEqual(app.debug, False)
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_cases(self):
        db.session.commit()
        db.drop_all()
        db.create_all()

        citizen = Citizen(citizen_id='66666666', name='Big Boi', score=1000)
        citizen.set_password('iambig')
        self.assertTrue(citizen.check_password('iambig'))

        db.session.add(citizen)
        db.session.commit()

    def test_citizens(self):
        self.assertEqual(Citizen.query.count(), 1)
        another = Citizen(citizen_id='11111', name='Smol Boi', score=1000)
        db.session.add(another)
        db.session.commit()
        self.assertEqual(Citizen.query.count(), 2)
    
    def test_report(self):
        report = Report()
    
    def test_index(self):
        res = self.app.get('/', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        

if __name__ == '__main__':
    unittest.main()