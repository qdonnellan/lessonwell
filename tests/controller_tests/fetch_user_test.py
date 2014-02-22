from tests.main_test_handler import TestBase
from controllers.fetch_user import get_user_by_username, get_user_by_google_id
from models.user import User

class FetchUserTest(TestBase):
    '''
    test the implementation of the fetch user controllers
    '''

    def create_new_user(self, username, email, googleID):
        new_user = User()
        new_user.populate(
            username = username,
            googleID = googleID,
            email = email,
            )
        new_user.put()

    def test_get_user_by_username(self):
        '''
        test the get_user_by_username controller
        '''
        self.create_new_user('foobar', 'foobar@gmail.com', '12345678')
        fetched_user= get_user_by_username('foobar')
        self.assertEqual(fetched_user.email, 'foobar@gmail.com')

    def test_get_user_by_google_id(self):
        self.create_new_user('foobar', 'foobar@gmail.com', '12345678')
        fetched_user= get_user_by_google_id('12345678')
        self.assertEqual(fetched_user.email, 'foobar@gmail.com')





