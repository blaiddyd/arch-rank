import os
import unittest
from app import app, db
from app.models import Citizen, Report, Status
from flask import url_for, abort
import string
import random


def gen_id():
    chars = string.digits
    return int(''.join(random.choice(chars) for _ in range(0, 6)))


class Tests(unittest.TestCase):
    # Test setup functions
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

    # Tests for database models
    def test_citizens(self):
        self.assertEqual(Citizen.query.count(), 0)
        another = Citizen(citizen_id='11111', name='Smol Boi', score=1000)
        db.session.add(another)
        db.session.commit()
        self.assertEqual(Citizen.query.count(), 1)

    def test_report(self):
        self.assertEqual(Report.query.count(), 0)
        report = Report(
            reporter_id='66666666',
            reported_id='11111',
            report_id=gen_id(),
            body='Terrible mate.'
        )
        db.session.add(report)
        db.session.commit()
        self.assertEqual(Report.query.count(), 1)

    def test_status(self):
        self.assertEqual(Status.query.count(), 0)
        status = Status(
            citizen_id='2222',
            status_id=gen_id(),
            status_category='amazingness',
            body='im just too good'
        )
        db.session.add(status)
        db.session.commit()
        self.assertEqual(Status.query.count(), 1)

    # Tests for application views
    def test_index(self):
        res = self.app.get('/', follow_redirects=True)
        self.assertEqual(res.status_code, 200)

    def test_login(self):
        res = self.app.get('/login', follow_redirects=True)
        self.assertEqual(res.status_code, 200)

    def test_logout(self):
        logout = '/logout'
        res = self.app.get(logout)
        self.assertEqual(res.status_code, 302)

    def test_feed(self):
        feed = '/feed'
        res = self.app.get(feed)
        self.assertEqual(res.status_code, 302)

    def test_rank(self):
        rank = '/rank'
        res = self.app.get(rank)
        self.assertEqual(res.status_code, 200)

    def test_user_profile(self):
        response = self.app.get('/profile/3434')
        self.assertEqual(response.status_code, 302)
        new_citizen = Citizen(citizen_id='3434', name='Good Boi', score=1000)
        db.session.add(new_citizen)
        db.session.commit()
        res = self.app.get('/profile/3434')
        self.assertEqual(Citizen.query.count(), 1)
        self.assertEqual(res.status_code, 302)
    
    def test_admin_board(self):
        resp = self.app.get('/admin_board')
        self.assertEqual(resp.status_code, 302)
    
    def test_eval(self):
        res = self.app.get('/evaluation')
        self.assertEqual(res.status_code, 302)


if __name__ == '__main__':
    unittest.main()
