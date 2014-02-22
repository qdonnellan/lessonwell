from tests.main_test_handler import TestBase
from models.user import User
import unittest

class UserModelTest(TestBase):
    '''
    test the implementation of the user model 
    '''

    def test_simple_creation_of_new_user(self):
        '''
        test a simple put() of a new user model 
        '''
        new_user = User()
        new_user.populate(
            username = 'foo',
            googleID = '123',
            email = 'user@example.com',
            )
        new_user.put()
        self.assertEqual(User.query().count(), 1)