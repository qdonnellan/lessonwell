from tests.main_test_handler import TestBase
from controllers.modify_content import new_content
from controllers.fetch_content import get_all_content
from models.user import User
from models.content import Content

import json

class GetContentTest(TestBase):
    '''
    test get requests to the api for content
    '''

    def create_sample_course_framework(self, num_courses, num_units, num_lessons):
        '''
        create a user, courses, units, and lessons for the purpose of testing the api
        '''
        user = self.create_and_return_local_user()
        for course in range(num_courses):
            new_content(title='Foo Course %s' % course, body='bar', contentType='course', parentKEY = user.key)
        
        courses = get_all_content(parentKEY = user.key, contentType = 'course')
        for course in courses:
            for unit in range(num_units):
                new_content(title='Foo Unit %s' % course, body='bar', contentType='unit', parentKEY = course.key)

        units = get_all_content(parentKEY = course.key, contentType = 'unit')
        for unit in units:
            for lesson in range(num_lessons):
                new_content(title='Foo Lesson %s' % lesson, body='bar', contentType='lesson', parentKEY = unit.key)

    def test_that_get_public_course_is_json_a_response(self):
        '''
        assert that the response from /api/1/1 is a json response
        '''
        response = self.testapp.get('/api/1/1')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_get_public_course(self):
        '''
        test api response for a request of a publically available course 
        at /api/{{userID}}/{{courseID}}

        we'll first create a bunch of course material, then we'll determine the id
        of the first user and their first course that was generated
        '''
        self.create_sample_course_framework(1,1,1)
        user_id = User.query().get().key.id()
        course_id = Content.query().get().key.id()
        response = self.testapp.get('/api/%s/%s' % (user_id, course_id))
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.body)
        self.assertEqual(data['title'], 'Foo Course 1')
        self.assertEqual(data['contentType'], 'course')
        self.assertEqual(data['body'], 'bar')






