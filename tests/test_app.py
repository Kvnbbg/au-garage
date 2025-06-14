import unittest
from datetime import datetime, timedelta
from flask import Flask, current_app
from app import create_app, db
from app.models import User, Role, ActivityLog, VisitCount

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing forms
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

class UserModelTestCase(BasicTestCase):
    def test_password_setter(self):
        u = User(username='john', email='john@example.com', password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(username='john', email='john@example.com', password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(username='john', email='john@example.com', password='cat')
        self.assertTrue(u.check_password('cat'))
        self.assertFalse(u.check_password('dog'))

    def test_password_salts_are_random(self):
        u = User(username='john', email='john@example.com', password='cat')
        u2 = User(username='susan', email='susan@example.com', password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_create_user_and_retrieve(self):
        role = Role(name='User')
        db.session.add(role)
        db.session.commit()
        u = User(username='testuser', email='test@example.com', password='password123', role_id=role.id)
        db.session.add(u)
        db.session.commit()
        retrieved_user = User.find_by_username('testuser')
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, 'test@example.com')

class RoleModelTestCase(BasicTestCase):
    def test_create_role_and_find(self):
        Role.create_role('Admin')
        retrieved_role = Role.find_by_name('Admin')
        self.assertIsNotNone(retrieved_role)
        self.assertEqual(retrieved_role.name, 'Admin')

class ActivityLogModelTestCase(BasicTestCase):
    def test_log_activity(self):
        role = Role(name='User')
        db.session.add(role)
        db.session.commit()
        u = User(username='logger', email='logger@example.com', password='logpassword', role_id=role.id)
        db.session.add(u)
        db.session.commit()
        ActivityLog.log_activity(user_id=u.id, activity_data='Logged in')
        log_entry = ActivityLog.query.filter_by(user_id=u.id).first()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.activity_data, 'Logged in')
        self.assertIsNotNone(log_entry.timestamp)

class MaintenanceDateTestCase(BasicTestCase):
    def test_home_page_uses_config_maintenance_date(self):
        test_date_str = '2025-01-01 10:00:00'
        self.app.config['MAINTENANCE_START_DATE'] = test_date_str
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_date_str, response.get_data(as_text=True))

    def test_home_page_fallback_date_missing_config(self):
        # Ensure the key is not in config for this test
        if 'MAINTENANCE_START_DATE' in self.app.config:
            del self.app.config['MAINTENANCE_START_DATE']

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check for the default date used in routes.py or a flash message indicating fallback
        # The exact default date is '2024-01-01 00:00:00'
        html_content = response.get_data(as_text=True)
        self.assertIn('MAINTENANCE_START_DATE not configured. Using default: 2024-01-01 00:00:00', html_content)
        self.assertIn('2024-01-01 00:00:00', html_content)


    def test_home_page_fallback_date_invalid_format(self):
        self.app.config['MAINTENANCE_START_DATE'] = 'invalid-date-format'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html_content = response.get_data(as_text=True)
        self.assertIn('Invalid MAINTENANCE_START_DATE format. Using default: 2024-01-01 00:00:00', html_content)
        self.assertIn('2024-01-01 00:00:00', html_content)

class VisitCountTestCase(BasicTestCase):
    def test_new_user_visit_recorded(self):
        with self.app.test_client() as client:
            client.get('/') # First visit
            cookie_obj = client.get_cookie('user_id')
            self.assertIsNotNone(cookie_obj, "user_id cookie was not set")
            user_id_cookie_val = cookie_obj.value

            visit_record = VisitCount.query.filter_by(user_id_str=user_id_cookie_val).first()
            self.assertIsNotNone(visit_record)
            self.assertEqual(visit_record.visits, 1)

    def test_existing_user_visit_incremented(self):
        user_id = 'test_user_123'
        # Simulate first visit by creating a record
        initial_visit_record = VisitCount(user_id_str=user_id, visits=1)
        db.session.add(initial_visit_record)
        db.session.commit()

        with self.app.test_client() as client:
            # Set cookie for the test client to simulate existing user
            client.set_cookie('user_id', user_id) # Corrected set_cookie
            client.get('/') # Second visit

            visit_record = VisitCount.query.filter_by(user_id_str=user_id).first()
            self.assertIsNotNone(visit_record)
            self.assertEqual(visit_record.visits, 2)

            client.get('/') # Third visit
            visit_record = VisitCount.query.filter_by(user_id_str=user_id).first()
            self.assertIsNotNone(visit_record)
            self.assertEqual(visit_record.visits, 3)

    def test_leaderboard_correct_no_visits(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # The first visitor immediately becomes the top visitor with 1 visit.
        self.assertIn("🏆 You&#39;re the top visitor with 1 visits!", response.get_data(as_text=True))

    def test_leaderboard_correct_with_visits(self):
        # User 1 visits 3 times
        u1 = VisitCount(user_id_str='user1', visits=3)
        db.session.add(u1)
        # User 2 visits 5 times (top visitor)
        u2 = VisitCount(user_id_str='user2_top', visits=5)
        db.session.add(u2)
        # User 3 visits 1 time
        u3 = VisitCount(user_id_str='user3', visits=1)
        db.session.add(u3)
        db.session.commit()

        # Current user (simulated by cookie) is user1
        with self.app.test_client() as client:
            client.set_cookie('user_id', 'user1') # Corrected set_cookie
            response = client.get('/') # This will increment user1's visits to 4

            html_content = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)

            # user1 should now have 4 visits. user2_top still has 5.
            # Expected message for user1:
            # "You're ranked below the top visitor (user2_top), who has 5 visits. You've completed X% of the top user's visits. Keep it up!"
            # X = floor((4/5)*100) = floor(80) = 80
            self.assertIn("You&#39;re ranked below the top visitor (user2_top), who has 5 visits.", html_content)
            self.assertIn("You&#39;ve completed 80% of the top user&#39;s visits. Keep it up!", html_content)

            # Simulate visit from the top user (user2_top)
            client.set_cookie('user_id', 'user2_top') # Corrected set_cookie
            response_top_user = client.get('/') # This will increment user2_top's visits to 6
            html_content_top_user = response_top_user.get_data(as_text=True)
            self.assertIn("🏆 You&#39;re the top visitor with 6 visits!", html_content_top_user)


if __name__ == '__main__':
    unittest.main()
