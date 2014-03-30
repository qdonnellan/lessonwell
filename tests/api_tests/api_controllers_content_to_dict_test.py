from tests.main_test_handler import TestBase
from controllers.new_course import new_course
from controllers.fetch_curriculum import get_content_by_id
from models.user import User

from api.api_controllers.content_to_dict import content_to_dict

class ContentToDictTest(TestBase):
    """
    test the implementation of the content model to 
    dictionary object controllers
    """

    def test_simple_content_model_conversion(self):
        """
        create a simple model and pass it to the content_to_dict controller
        """
        local_user = self.create_and_return_local_user()
        course_id = new_course({
            'teacher' : local_user.key.id(),
            'title' : 'foo course',
            'body' : 'hey look mom',
            })
        course = get_content_by_id(course_id)
        dict_content = content_to_dict(course)
        self.assertEqual(dict_content['content_type'], 'course')
        self.assertEqual(dict_content['content']['title'], 'foo course')
