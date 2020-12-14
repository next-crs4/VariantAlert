from django.test import TestCase, Client

from django.contrib.auth.models import User

class AccountTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='test-user',
                                        email='test.user@example.com',
                                        password="test-password")

    def _login(self):
        self.client.force_login(self.user)

    def test_signup(self):
        self.client.post("/accounts/signup",
                         dict(username='test-user-1',
                              email='test.user1@example.com',
                              password1="testpassword",
                              password2="testpassword")
                         )
        user = User.objects.filter(username='test-user-1').values()[0]
        self.assertEqual(user.get('username'), 'test-user-1')
        self.assertEqual(user.get('email'), 'test.user1@example.com')

    def test_login(self):
        resp = self.client.post("/variants/login/",
                                dict(username='test-user',
                                     password='test-password')
                                )
        self.assertIs(resp.status_code, 200)


    def test_edit_user(self):
        self._login()
        self.client.post("/accounts/update/1",
                         dict(username='test',
                              email='test@test.com')
                        )
        user = User.objects.filter(username='test').values()[0]
        self.assertEqual(user.get('username'), 'test')
        self.assertEqual(user.get('email'), 'test@test.com')