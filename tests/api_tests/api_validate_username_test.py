from tests.main_test_handler import TestBase
import json

class ValidateUsernameAPITest(TestBase):
    '''
    test the implementation of the validate username api
    '''

    def test_request_with_protected_username(self):
        '''
        a username that is on the protected list should return an error message
        '''
        response = self.testapp.get('/api/validate_username/%s' % 'admin')
        data = json.loads(response.body)
        self.assertIsNotNone(data['error'])
        self.assertEqual(data['error'], "That username is protected, choose a different one")

    def test_request_with_short_username(self):
        '''
        a username that is too short should return a length error
        '''
        response = self.testapp.get('/api/validate_username/%s' % 'aaa')
        data = json.loads(response.body)
        self.assertIsNotNone(data['error'])
        self.assertEqual(data['error'], "Your username must be at least 5 characters and no more than 20")

    def test_request_with_long_username(self):
        '''
        a username that is too long should return a length error
        '''
        response = self.testapp.get('/api/validate_username/%s' % 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        data = json.loads(response.body)
        self.assertIsNotNone(data['error'])
        self.assertEqual(data['error'], "Your username must be at least 5 characters and no more than 20")

    def test_request_with_invalid_chars_username(self):
        '''
        a username that contains invalid characters should be rejected
        '''
        response = self.testapp.get('/api/validate_username/%s' % str('user_asdas__'))
        data = json.loads(response.body)
        self.assertIsNotNone(data['error'])
        self.assertEqual(data['error'], "Your username may only contain numbers and letters")

    def test_request_with_non_unique_username(self):
        '''
        a username that contains invalid characters should be rejected
        '''
        user = self.create_and_return_local_user(username='user111')
        response = self.testapp.get('/api/validate_username/%s' % 'user111')
        data = json.loads(response.body)
        self.assertIsNotNone(data['error'])
        self.assertEqual(data['error'], "That username is already taken")

    def test_request_with_valid_username(self):
        '''
        a username that is valid should return no error
        '''
        response = self.testapp.get('/api/validate_username/%s' % 'user123')
        data = json.loads(response.body)
        self.assertFalse(data['error'])



