from tests.main_test_handler import TestBase
from controllers.new_course import new_course
import json

class GetUserAPITest(TestBase):
    """
    test the implementation of the user api
    """

    def test_simple_user_fetch(self):
        """
        fetch a known user with an api get request
        """
        user = self.create_and_return_local_user(username='foouser')
        user_id = user.key.id()
        response = self.testapp.get('/api/user/%s' % user_id)
        json_user = json.loads(response.body)
        self.assertEqual(json_user['username'], 'foouser')

    def test_user_fetch_for_not_existing_user(self):
        """
        fetch a user that is known to not exist
        """
        response = self.testapp.get('/api/user/9999999')
        json_user = json.loads(response.body)
        self.assertEqual(json_user['error'], 'that user does not exist')

    def test_user_with_courses(self):
        """
        create a user + a course and see that the course
        is actually appended to the user's json object
        """
        teacher = self.create_and_return_local_user(username='foouser')
        user_id = teacher.key.id()
        content = {
            'teacher' : int(teacher.key.id()),
            'title' : 'foo course',
            'body' : 'study hard, learn well, duh',
        }
        course_id = new_course(content)
        response = self.testapp.get('/api/user/%s' % user_id)
        user_data = json.loads(response.body)
        user_courses = user_data['courses']
        self.assertIn(str(course_id), user_courses)

    def test_fetch_current_user(self):
        """
        make a call to '/api/user' with no id specified the get
        implies a request for the current user
        """
        self.create_google_user(user_id = '123')
        teacher = self.create_and_return_local_user(googleID = '123')
        teacher_id = teacher.key.id()
        response = self.testapp.get('/api/user')
        user_data = json.loads(response.body)
        self.assertNotIn('error', user_data)
        self.assertEqual(user_data['id'], teacher_id)



        



