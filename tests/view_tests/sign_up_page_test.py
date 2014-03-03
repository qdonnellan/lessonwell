from tests.main_test_handler import TestBase
from models.user import User
import json
import unittest

class SignUpPageTest(TestBase):
    '''
    test that the sign up page is working correctly
    '''

    def test_sign_up_page_view_not_authenticated(self):
        '''
        test views of '/sign_up'
        '''
        response = self.testapp.get('/sign_up')
        self.assertEqual(response.status_int, 302)

    def test_sign_up_page_view_with_google_authentication(self):
        '''
        test views of '/sign_up' with a user authenticated to google
        '''
        self.create_google_user()
        response = self.testapp.get('/sign_up')
        self.assertEqual(response.status_int, 200)

    def test_sign_up_page_post_without_authentication(self):
        '''
        a post request from a non autenticated user should be aborted
        '''
        response = self.testapp.post('/sign_up', status=401)
        self.assertEqual(response.status_int, 401)

    def test_sign_up_page_post_request_without_token(self):
        '''
        a post request without the correct stripe token should fail
        '''
        self.create_google_user()
        data = { 'username' : 'legitimateUsername' }
        response = self.testapp.post('/sign_up', data)
        self.assertIn('Invalid Payment Information', response.follow().body)

    def test_sign_up_page_with_protected_username(self):
        '''
        a post request using a protected username should be rejected
        '''
        self.create_google_user()
        data = { 'username' : 'admin' }
        response = self.testapp.post('/sign_up', data)
        self.assertIn('That username is protected, choose a different one', response.follow().body)

    def test_sign_up_page_with_non_unique_username(self):
        '''
        a post request using a username that is already taken should be rejected
        '''
        self.create_and_return_local_user(username='helloworld')
        self.create_google_user()
        data = { 'username' : 'helloworld' }
        response = self.testapp.post('/sign_up', data)
        self.assertIn('That username is already taken', response.follow().body)

    @unittest.skip('skipping this test for now as it creates a new user on stripe')
    def test_valid_sign_up_post(self):
        self.create_google_user()
        self.assertEqual(User.query().count(), 0)
        data = {
            'username' : 'helloworld',
            'stripeToken' : self.generate_sample_token().id,
            }
        response = self.testapp.post('/sign_up', data)
        self.assertEqual(User.query().count(), 1) #there should be a new user in the database!
        self.assertIn('You have successfully created a lessonwell account', response.follow().body)








