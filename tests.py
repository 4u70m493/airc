from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Event


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_plan(self):
        u1 = User(username='john', email='john@example.com')
        p1 = Event(name="Conference", from_ts=datetime.utcnow() + timedelta(seconds=4),
                   to_ts=datetime.utcnow() + timedelta(seconds=10),
                   city='MOW',
                   country='RU',
                   location='Museum')


        print("Add user and event, commit")
        db.session.add(u1)
        db.session.add(p1)
        db.session.commit()

        self.assertEqual(u1.planned.all(), [])

        u1.plan(p1)
        print("User plans event - commit")
        db.session.commit()
        self.assertTrue(u1.is_planning(p1))
        self.assertEqual(u1.planned.count(), 1)
        self.assertEqual(u1.planned.first().country, 'RU')

        u1.unplan(p1)
        print("User unplans event - commit")
        db.session.commit()
        self.assertFalse(u1.is_planning(p1))
        self.assertEqual(u1.planned.count(), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)