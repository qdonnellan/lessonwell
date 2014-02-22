from tests.main_test_handler import TestBase
from controllers.modify_user import new_user, edit_user
from models.user import User


class ModifyUserTest(TestBase):
    '''
    test the modify user controller functions
    '''

    def test_new_user_implementation(self):
        '''
        test that the new user controller is working correctly
        '''
        new_user('jamesusername', 'James Smith', 'james@example.com', '12345678')
        self.assertEqual(User.query().count(), 1)
        new_user('foobar', 'James Smith', 'james@example.com', '2')
        self.assertEqual(User.query().count(), 2)

    def test_new_user_bad_username(self):
        '''
        a new user with a bad username should raise a NameError exception
        '''
        self.assertRaises(NameError, new_user, 'james-username', 'James Smith', 'james@example.com', '12345678')

    def test_new_user_non_unique_username(self):
        '''
        a new user with a username that already exists shoudl raise a NameError
        '''
        new_user('jamesusername', 'James Smith', '1@example.com', '1')
        self.assertEqual(User.query().count(), 1)
        self.assertRaises(NameError, new_user, 'jamesusername', 'Bill Bradley', '2@example.com', '2')
        self.assertEqual(User.query().count(), 1)



        