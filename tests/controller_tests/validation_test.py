from tests.main_test_handler import TestBase
from controllers.validation import validate_username
from controllers.modify_user import new_user

class ValidationTest(TestBase):
    '''
    test the validation controller is operating correctly
    '''
    def test_username_with_bad_characters(self):
        '''
        a username should only contain numbers and letters
        '''
        self.assertRaises(NameError, validate_username, 'bad_username&&')

    def test_username_is_protected(self):
        '''
        a username cannot belong in the protected list
        '''
        self.assertRaises(NameError, validate_username, 'admin')

    def test_username_is_too_short(self):
        '''
        a username must be between 5 and 20 characters
        '''
        self.assertRaises(NameError, validate_username, 'foo')

    def test_username_is_too_long(self):
        '''
        a username must be between 5 and 20 characters
        '''
        self.assertRaises(NameError, validate_username, 'foofoofoofoofoofoofoofoofoofoofoofoofoofoofoo')

    def test_username_is_not_unique(self):
        '''
        a username must not be the same as someone else's
        '''
        new_user('jamesusername', 'James Smith', 'james1@example.com', '1')
        self.assertRaises(NameError, new_user, 'jamesusername', 'James Smith', 'james2@example.com', '2')







        