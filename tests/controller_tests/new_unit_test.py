from tests.main_test_handler import TestBase
from google.appengine.ext import ndb
from controllers.new_course import new_course
from controllers.new_unit import new_unit

from models.curriculum import Curriculum 

class NewUnitTest(TestBase):
    """
    test the implementation of the new unit function
    """

    def test_new_unit_creation(self):
        """
        assert that a new unit can be created using the new unit function
        """
        local_user = self.create_and_return_local_user()
        course_id = new_course({
            'teacher' : local_user.key.id(),
            'title' : 'foo course',
            'body' : 'hey look mom',
            })
        unit_id = new_unit({
            'course' : course_id, 
            'title' : 'foo unit',
            'body' : 'bla bla unit body',
            })
        unit = ndb.Key('Curriculum', unit_id).get()
        course = ndb.Key('Curriculum', course_id).get()
        # check that the correct content properties were set
        self.assertEqual(unit.content['title'], 'foo unit')
        self.assertEqual(unit.content['body'], 'bla bla unit body')
        # check that the correct inferred properties were set
        self.assertEqual(unit.content['course'], course_id)
        self.assertEqual(unit.content['teacher'], int(local_user.key.id()))
        self.assertEqual(unit.content_type, 'unit')
        # check that the parent course correctly had this new unit id appended
        self.assertIn(unit_id, course.content['units'])

    def test_new_unit_with_bad_course_id(self):
        """
        creating a new unit with a bad course id reference should fail
        """
        content = {
            'course' : 99999999,
            'title' : 'bla', 
            'body' : 'bla',
            }
        self.assertRaises(Exception, new_unit, content)
