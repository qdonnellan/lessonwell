from tests.main_test_handler import TestBase
from google.appengine.ext import ndb
from controllers.new_course import new_course
from controllers.new_unit import new_unit
from controllers.new_lesson import new_lesson
from models.curriculum import Curriculum 

class NewLessonTest(TestBase):
    """
    test the implementation of the new lesson function
    """

    def test_new_lesson_creation(self):
        """
        assert that a new lesson can be created using the new lesson function
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
        lesson_id = new_lesson({
            'unit' : unit_id, 
            'title' : 'foo lesson',
            'body' : 'lesson about stuff'
            })
        unit = ndb.Key('Curriculum', unit_id).get()
        course = ndb.Key('Curriculum', course_id).get()
        lesson = ndb.Key('Curriculum', lesson_id).get()

        # check that the correct content properties were set
        self.assertEqual(lesson.content['title'], 'foo lesson')
        self.assertEqual(lesson.content['body'], 'lesson about stuff')
        # check that the correct inferred properties were set
        self.assertEqual(lesson.content['course'], course_id)
        self.assertEqual(lesson.content['unit'], unit_id)
        self.assertEqual(lesson.content['teacher'], int(local_user.key.id()))
        self.assertEqual(lesson.content_type, 'lesson')
        # check that the parent unit correctly had this new lesson appended
        self.assertIn(lesson_id, unit.content['lessons'])

    def test_new_lesson_with_bad_unit_id(self):
        """
        creating a new unit with a bad course id reference should fail
        """
        content = {
            'unit' : 900000991212,
            'title' : 'bla', 
            'body' : 'bla',
            }
        self.assertRaises(Exception, new_lesson, content)
