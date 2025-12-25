import unittest
from datetime import datetime
from flask import current_app
from app import create_app, db
from app.models import User, Role, ActivityLog, VisitCount
from config import DATE_FORMAT, DEFAULT_MAINTENANCE_START_DATE

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                "WTF_CSRF_ENABLED": False,
                "SERVER_NAME": "localhost.localdomain",
            }
        )
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        from app.models import init_roles # Import and call init_roles here
        init_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def _register_user(self, username, email, password, follow_redirects=True):
        return self.client.post(current_app.url_for('auth.register'), data={
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': password
        }, follow_redirects=follow_redirects)

    def _login_user(self, username, password, follow_redirects=True):
        return self.client.post(current_app.url_for('auth.login'), data={
            'username': username,
            'password': password
        }, follow_redirects=follow_redirects)

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
        # init_roles in BasicTestCase.setUp already creates 'Admin', 'Client', etc.
        # Test creating a new, unique role here.
        unique_role_name = "TestSpecificRole"
        created_role = Role.create_role(unique_role_name, "grey", "#testspecific")
        self.assertIsNotNone(created_role)
        self.assertEqual(created_role.name, unique_role_name)
        self.assertEqual(created_role.color_code, "grey")
        self.assertEqual(created_role.hashtag, "#testspecific")

        retrieved_role = Role.find_by_name(unique_role_name)
        self.assertIsNotNone(retrieved_role)
        self.assertEqual(retrieved_role.name, unique_role_name)

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
        test_date = datetime(2025, 1, 1, 10, 0, 0)
        self.app.config['MAINTENANCE_START_DATE'] = test_date
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_date.strftime(DATE_FORMAT), response.get_data(as_text=True))

    def test_home_page_fallback_date_missing_config(self):
        # Ensure the key is not in config for this test
        if 'MAINTENANCE_START_DATE' in self.app.config:
            del self.app.config['MAINTENANCE_START_DATE']

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check for the default date used in routes.py or a flash message indicating fallback
        html_content = response.get_data(as_text=True)
        self.assertIn(
            f"Maintenance schedule not configured. Showing default start date. "
            f"{DEFAULT_MAINTENANCE_START_DATE.strftime(DATE_FORMAT)}.",
            html_content,
        )
        self.assertIn(DEFAULT_MAINTENANCE_START_DATE.strftime(DATE_FORMAT), html_content)


    def test_home_page_fallback_date_invalid_format(self):
        self.app.config['MAINTENANCE_START_DATE'] = 'invalid-date-format'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html_content = response.get_data(as_text=True)
        self.assertIn(
            "Maintenance schedule is invalid. Using the default start date.",
            html_content,
        )
        self.assertIn(DEFAULT_MAINTENANCE_START_DATE.strftime(DATE_FORMAT), html_content)

class VisitCountTestCase(BasicTestCase):
    def test_new_user_visit_recorded(self):
        with self.app.test_client() as client:
            client.get('/') # First visit
            # Try to get cookie, specifying domain if SERVER_NAME is set
            cookie_obj = client.get_cookie('user_id', domain=self.app.config.get('SERVER_NAME', 'localhost'))
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
            client.set_cookie('user_id', user_id, domain=self.app.config['SERVER_NAME'])
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
            client.set_cookie('user_id', 'user1', domain=self.app.config['SERVER_NAME'])
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
            client.set_cookie('user_id', 'user2_top', domain=self.app.config['SERVER_NAME'])
            response_top_user = client.get('/') # This will increment user2_top's visits to 6
            html_content_top_user = response_top_user.get_data(as_text=True)
            self.assertIn("🏆 You&#39;re the top visitor with 6 visits!", html_content_top_user)

class AuthFeaturesTestCase(BasicTestCase):
    def test_visual_login_indicator_logged_out(self):
        response = self.client.get(current_app.url_for('main.home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('<span class="login-indicator logged-out"></span>', response.get_data(as_text=True))
        self.assertNotIn('<span class="login-indicator logged-in"></span>', response.get_data(as_text=True))

    # _register_user and _login_user moved to BasicTestCase

    def test_visual_login_indicator_logged_in(self):
        self._register_user('testloginuser', 'login@example.com', 'Password123!')
        # After registration, user is logged in and redirected to dashboard
        # So, access home page again to check indicator
        response = self.client.get(current_app.url_for('main.home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('<span class="login-indicator logged-in"></span>', response.get_data(as_text=True))
        self.assertNotIn('<span class="login-indicator logged-out"></span>', response.get_data(as_text=True))
        # Logout to clean up session for next test
        self.client.get(current_app.url_for('auth.logout'))

    def test_login_redirects_to_dashboard(self):
        self._register_user('loginredirect', 'loginredirect@example.com', 'Password123!')
        self.client.get(current_app.url_for('auth.logout')) # Log out first

        response = self.client.post(current_app.url_for('auth.login'), data={
            'username': 'loginredirect',
            'password': 'Password123!'
        }, follow_redirects=False) # Important: don't follow redirects to check Location
        self.assertEqual(response.status_code, 302)
        # Compare path part of the URL
        expected_path = current_app.url_for('auth.dashboard', _external=False)
        self.assertEqual(response.location, expected_path)


    def test_register_redirects_to_dashboard_and_logs_in(self):
        response = self.client.post(current_app.url_for('auth.register'), data={
            'username': 'regredirect',
            'email': 'regredirect@example.com',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        }, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        expected_path = current_app.url_for('auth.dashboard', _external=False)
        self.assertEqual(response.location, expected_path)

        # Verify user is logged in by accessing a protected route or checking session
        # Accessing home and checking for logged-in indicator is an indirect way
        home_response = self.client.get(current_app.url_for('main.home'))
        self.assertIn('<span class="login-indicator logged-in"></span>', home_response.get_data(as_text=True))
        self.client.get(current_app.url_for('auth.logout')) # Clean up

    def test_rate_limiting_on_login_route(self):
        # The login route is limited to 10 per minute.
        # We will make 10 requests, which should succeed.
        # The 11th request should fail with a 429 status code.
        login_url = current_app.url_for('auth.login')
        for i in range(10):
            response = self.client.get(login_url)
            self.assertNotEqual(response.status_code, 429, f"Request {i+1} should not be rate limited.")

        # The 11th request should be rate limited.
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 429, "The 11th request should be rate limited.")


    def test_edit_profile_form_validation(self):
        from app.auth.forms import EditProfileForm
        # Create initial user
        u1 = User(username='userone', email='userone@example.com', password='Password123!')
        db.session.add(u1)
        db.session.commit()
        # Create another user for conflict testing
        u2 = User(username='usertwo', email='usertwo@example.com', password='Password123!')
        db.session.add(u2)
        db.session.commit()

        # Login as userone
        self._login_user('userone', 'Password123!')

        # 1. Test changing username/email to something new and unique
        form = EditProfileForm(original_username=u1.username, original_email=u1.email, username='newuserone', email='newuserone@example.com')
        self.assertTrue(form.validate())

        # 2. Test changing username to an existing one used by *another* user (should fail)
        form = EditProfileForm(original_username=u1.username, original_email=u1.email, username='usertwo', email='userone@example.com')
        self.assertFalse(form.validate())
        self.assertIn('username', form.errors)
        self.assertIn('This username is already taken', form.errors['username'][0])

        # 3. Test changing email to an existing one used by *another* user (should fail)
        form = EditProfileForm(original_username=u1.username, original_email=u1.email, username='userone', email='usertwo@example.com')
        self.assertFalse(form.validate())
        self.assertIn('email', form.errors)
        self.assertIn('That email is already in use. Please choose a different one.', form.errors['email'][0])

        # 4. Test keeping the *same* username/email (should pass)
        form = EditProfileForm(original_username=u1.username, original_email=u1.email, username='userone', email='userone@example.com')
        self.assertTrue(form.validate())

        # 5. Test submitting form with no changes (should pass)
        # In the route, data is typically populated from current_user for GET request
        # Here we simulate form submission with data identical to original
        with self.client.session_transaction() as sess:
             # Ensure user is logged in for current_user context in form if it were live
             # For direct form testing, we manually pass original values
             pass

        form = EditProfileForm(data={'username': u1.username, 'email': u1.email}, original_username=u1.username, original_email=u1.email)
        self.assertTrue(form.validate())

        # 6. Test empty username (should fail DataRequired)
        form = EditProfileForm(original_username=u1.username, original_email=u1.email, username='', email='userone@example.com')
        self.assertFalse(form.validate())
        self.assertIn('username', form.errors)

        # 7. Test invalid email format
        form = EditProfileForm(original_username=u1.username, original_email=u1.email, username='userone', email='notanemail')
        self.assertFalse(form.validate())
        self.assertIn('email', form.errors)

        self.client.get(current_app.url_for('auth.logout')) # Clean up

class RoleAndContextProcessorTestCase(BasicTestCase):
    def setUp(self):
        super().setUp()
        # init_roles() is now called in BasicTestCase.setUp(), no need to repeat here
        # from app.models import init_roles
        # init_roles()

    def test_roles_created_with_attributes(self):
        expected_roles = [
            {'name': 'Admin', 'color_code': 'yellow', 'hashtag': '#admin'},
            {'name': 'Maintenance', 'color_code': 'darkgrey', 'hashtag': '#maintenance'},
            {'name': 'Worker', 'color_code': 'blue', 'hashtag': '#worker'},
            {'name': 'Client', 'color_code': 'green', 'hashtag': '#client'}
        ]
        for role_data in expected_roles:
            role = Role.find_by_name(role_data['name'])
            self.assertIsNotNone(role, f"Role {role_data['name']} not found.")
            self.assertEqual(role.color_code, role_data['color_code'])
            self.assertEqual(role.hashtag, role_data['hashtag'])

    def test_context_processor_logged_out_user(self):
        with self.client:
            self.client.get(current_app.url_for('main.home')) # Make a request to establish context
            # For context processor tests, it's easier to test its direct output
            # by invoking it within a test request context if direct context access is tricky.
            # Or, check its effect in a rendered template if a variable is always present.
            # Here, we'll test it more directly if possible, or via template variable.
            # Since current_user is not authenticated, user_role should be None.
            # We can't directly access template context easily without rendering.
            # Let's check if a template renders something specific when user_role is None.
            # For now, this test will be conceptual or rely on checking a page that uses user_role.
            # A simpler way: call the context processor function directly.
            from app import create_app # to get access to the app factory again
            temp_app = create_app() # Create a temporary app instance for the test
            # Find the context processor
            cp_func = None
            for func in temp_app.template_context_processors[None]: # None is for app-wide CPs
                if func.__name__ == 'inject_user_role_info':
                    cp_func = func
                    break
            self.assertIsNotNone(cp_func, "Context processor inject_user_role_info not found.")

            # Simulate app context for the processor
            with temp_app.test_request_context('/'):
                # current_user will be AnonymousUserMixin, not authenticated
                context = cp_func()
                self.assertIn('user_role', context)
                self.assertIsNone(context['user_role'])


    def test_context_processor_logged_in_user_with_role(self):
        # Create a role and user
        admin_role = Role.find_by_name('Admin')
        if not admin_role: # Should be created by init_roles in setUp
            admin_role = Role.create_role('Admin', 'yellow', '#admin')

        test_user = User(username='roleuser', email='roleuser@example.com', password='Password123!', role_id=admin_role.id)
        db.session.add(test_user)
        db.session.commit()

        # Log in the user
        self.client.post(current_app.url_for('auth.login'), data={
            'username': 'roleuser',
            'password': 'Password123!'
        }, follow_redirects=True)

        # Access a page that uses base.html (like home) and check for role attributes
        response = self.client.get(current_app.url_for('main.home'))
        self.assertEqual(response.status_code, 200)
        html_content = response.get_data(as_text=True)

        # Check for Admin role's color_code in navbar style (yellow)
        # Note: The style might be background-color: yellow !important;
        self.assertIn('style="background-color: yellow', html_content)
        # Check for Admin role's hashtag
        self.assertIn(admin_role.hashtag, html_content) # #admin
        self.assertIn(f'<span class="badge badge-info role-hashtag">{admin_role.hashtag}</span>', html_content)

        self.client.get(current_app.url_for('auth.logout')) # Clean up

    def test_admin_can_change_own_role(self):
        from app.auth.forms import EditProfileForm # For form data keys

        admin_role = Role.find_by_name('Admin')
        worker_role = Role.find_by_name('Worker')
        self.assertIsNotNone(admin_role, "Admin role not found")
        self.assertIsNotNone(worker_role, "Worker role not found")

        backup_admin = User(
            username='adminbackup',
            email='adminbackup@example.com',
            password='Password123!',
            role_id=admin_role.id,
        )
        db.session.add(backup_admin)

        admin_user = User(username='admineditor', email='admineditor@example.com', password='Password123!', role_id=admin_role.id)
        db.session.add(admin_user)
        db.session.commit()

        self._login_user('admineditor', 'Password123!', follow_redirects=True) # Ensure follow_redirects if needed by test logic

        response = self.client.post(current_app.url_for('auth.profile'), data={
            'username': 'admineditor_newname', # Change username too
            'email': 'admineditor_newmail@example.com', # Change email too
            'role': worker_role.id # Change role to Worker
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200) # Should redirect to profile, then 200

        updated_admin_user = User.find_by_id(admin_user.id)
        self.assertEqual(updated_admin_user.role_id, worker_role.id)
        self.assertEqual(updated_admin_user.role.name, 'Worker')
        self.assertEqual(updated_admin_user.username, 'admineditor_newname')

        self.client.get(current_app.url_for('auth.logout'))


if __name__ == '__main__':
    unittest.main()
