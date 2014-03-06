from tests.main_test_handler import TestBase
from models.user import User
from api.api_controllers.user_to_dict import user_to_dict

class UserToDictTest(TestBase):
    '''
    test the implementation of the user model to dictionary object controllers
    '''

    def test_simple_user_model_conversion(self):
        '''
        create a simple user model and pass it to the content_to_dict controller
        '''
        sample_user = User(username='man', email='man@man.com', googleID='1').put()
        dict_user = user_to_dict(sample_user.get())
        self.assertEqual(dict_user['username'], 'man')
        self.assertEqual(dict_user['email'], 'man@man.com')
        self.assertEqual(dict_user['googleID'], '1')
