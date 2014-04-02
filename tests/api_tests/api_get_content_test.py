from tests.main_test_handler import TestBase
from controllers.new_course import new_course
from controllers.new_unit import new_unit
from controllers.new_lesson import new_lesson
from controllers.fetch_content import get_all_content
from controllers.fetch_content_by_id import get_course
from models.user import User
from models.curriculum import Curriculum
from models.approval import Approval

import json

class GetContentTest(TestBase):
    """
    test get requests to the api for content
    """

    def create_sample_course_framework(self,NC,NU,NL):
        """
        create a user, courses, units, and lessons
        for the purpose of testing the api

        NC is the number of courses to create
        NU is the number of units, 
        NL is the number of lessons
        """
        user = self.create_and_return_local_user()
        course_id_bank = []
        for course in range(NC):
            course_id = new_course({
                'title' : 'Foo Course %s' % course,
                'teacher' : user.key.id()
                })
            course_id_bank.append(course_id)

        unit_id_bank = []
        for course_id in course_id_bank:
            for unit in range(NU):
                unit_id = new_unit({
                    'title' : 'Foo Unit %s' % unit,
                    'course' : course_id
                    })
                unit_id_bank.append(unit_id)

        for unit_id in unit_id_bank:
            for lesson in range(NL):
                new_lesson({
                    'title' : 'Foo Lesson %s' % lesson,
                    'unit' : unit_id
                    })

    def test_that_get_public_course_is_a_json_response(self):
        """
        assert that the response from /api/curriculum/1 is a json response
        """
        response = self.testapp.get('/api/curriculum/1')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_get_bad_course(self):
        """
        an api request to a non-existing course should return an error message
        """
        response = self.testapp.get('/api/curriculum/91910191992')
        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.body)
        self.assertIn('error', data)

    def test_get_public_course(self):
        """
        test api response for a request of a publically available course
        at /api/curriculum{{courseID}}

        we'll first create a bunch of course material, then we'll determine 
        the id of the first user and their first course that was generated
        """
        self.create_sample_course_framework(1,1,1)
        user_id = User.query().get().key.id()
        course_id = Curriculum.query(
            Curriculum.content_type == 'course'
            ).get().key.id()
        response = self.testapp.get('/api/curriculum/%s' % course_id)
        self.assertEqual(response.status_int, 200)

        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.body)
        self.assertNotIn('error', data)
        self.assertEqual(data['id'], course_id)
        self.assertEqual(data['content']['title'], 'Foo Course 0')
        self.assertEqual(data['content_type'], 'course')

    def test_non_authenticated_get_private_course(self):
        """
        attempt to fetch a private course from a non-authenticated user

        non-authenticated means not logged into google
        """
        author = self.create_and_return_local_user()
        course_id = new_course({
            'title' : 'Foo Course',
            'teacher' : author.key.id(),
            'private' : True,
            })
        response = self.testapp.get(
            '/api/curriculum/%s' % course_id,
            )
        data = json.loads(response.body)
        self.assertIn('error', data)

    def test_non_authorized_get_private_course(self):
        """
        attempt to fetch a private course from authenticated/non-approved user

        non-approved means the user has a google account which has not
        been awarded access by the teacher
        """
        author = self.create_and_return_local_user()
        course_id = new_course({
            'title' : 'Foo Course',
            'teacher' : author.key.id(),
            'private' : True,
            })
        self.create_google_user()
        response = self.testapp.get(
            '/api/curriculum/%s' % course_id,
            )
        data = json.loads(response.body)
        self.assertIn('error', data)


