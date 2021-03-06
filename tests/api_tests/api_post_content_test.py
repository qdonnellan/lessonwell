from tests.main_test_handler import TestBase
from models.curriculum import Curriculum

import json

class PostContentTest(TestBase):
    """
    test post requests to the api for content
    """

    def test_simple_course_post(self):
        """
        pass a new course data to the post handler at /api/curriculum
        """
        self.create_google_user(user_id = '123')
        author = self.create_and_return_local_user(googleID = '123')
        data = {
            'title' : 'foo', 
            'body' : 'bar', 
            'content_type' : 'course',
            }
        response = self.testapp.post('/api/curriculum', data)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')
        response_data = json.loads(response.body)
        self.assertNotIn('error', response_data)
        self.assertEqual(response_data['content']['teacher'], author.key.id())

    def test_unauthorized_course_post(self):
        """
        attempt to create a new course as an unauthorized user
        """
        self.create_google_user()
        data = {
            'title' : 'foo', 
            'body' : 'bar', 
            'content_type' : 'course',
            }
        response = self.testapp.post('/api/curriculum', data, status=401)
        self.assertEqual(response.status_int, 401)

    def test_bad_course_type(self):
        """
        attempt a post request with a bad content_type passed
        """
        self.create_google_user(user_id = '123')
        author = self.create_and_return_local_user(googleID = '123')
        data = {
            'title' : 'foo', 
            'body' : 'bar', 
            'content_type' : 'GOBBLEDEEGOOP',
            }
        response = self.testapp.post('/api/curriculum', data)
        response_data = json.loads(response.body)
        self.assertIn('error', response_data)
        self.assertIn('invalid content type',response_data['error'])

    def test_create_new_course_then_modify_same_course(self):
        """
        create a new course then modify it 
        """
        self.create_google_user(user_id = '123')
        author = self.create_and_return_local_user(googleID = '123')
        data = {
            'title' : 'foo', 
            'body' : 'bar', 
            'content_type' : 'course',
            }
        response = self.testapp.post('/api/curriculum', data)
        self.assertEqual(Curriculum.query().count(), 1)
        response_data = json.loads(response.body)
        course_id = response_data['id']

        # now update the title and send another request
        data['title'] = 'updated foo'
        new_response = self.testapp.post(
            '/api/curriculum/%s' % course_id, 
            data
            )
        new_response_data = json.loads(response.body)
        self.assertNotIn('error', new_response_data)
        self.assertEqual(Curriculum.query().count(), 1)
        db_course = Curriculum.query().get()
        self.assertEqual(db_course.content['title'], 'updated foo')









