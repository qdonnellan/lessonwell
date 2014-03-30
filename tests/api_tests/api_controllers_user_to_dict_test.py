from tests.main_test_handler import TestBase
from models.user import User
from api.api_controllers.user_to_dict import user_to_dict

class UserToDictTest(TestBase):
    """
    test the implementation of the user_to_dict
    """

    def test_simple_user_model_conversion(self):
        """
        create a simple user model, pass to user_to_dict()
        assert resulting dictionary is correct
        """
        sample_user = User(
            username='man',
            email='man@man.com',
            googleID='1'
            ).put()
        dict_user = user_to_dict(sample_user.get())
        self.assertEqual(dict_user['username'], 'man')
        self.assertEqual(dict_user['email'], 'man@man.com')
        self.assertEqual(dict_user['googleID'], '1')
