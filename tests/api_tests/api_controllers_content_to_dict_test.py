from tests.main_test_handler import TestBase
from models.content import Content
from models.user import User
from api.api_controllers.content_to_dict import content_to_dict

class ContentToDictTest(TestBase):
    '''
    test the implementation of the content model to dictionary object controllers
    '''

    def test_simple_content_model_conversion(self):
        '''
        create a simple model and pass it to the content_to_dict controller
        '''
        sample_user = User(username='man', email='man@man.com', googleID='1').put()
        sample_content = Content(title='foo', body='bar', contentType='contentType', parent=sample_user).put()
        dict_content = content_to_dict(sample_content.get())
        self.assertEqual(dict_content['title'], 'foo')
        self.assertIsNone(dict_content['listed'])
