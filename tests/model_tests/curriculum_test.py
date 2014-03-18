from tests.main_test_handler import TestBase
from google.appengine.ext import ndb
from models.curriculum import Curriculum
import unittest

class CurriculumModelTest(TestBase):
    """
    test the implementation of the curriculum model 
    """

    def test_simple_creation_of_new_curriculum_model(self):
        """
        test a simple put() of a new curriculum model 
        """

        new_content = Curriculum()
        new_content.populate(
            content_type = 'course',
            content = {
                'title' : 'foo course',
                'owner' : 123,
                'units' : None
                }
            )
        key = new_content.put()

        fetched_content = ndb.Key(Curriculum, key.id()).get()
        self.assertEqual(fetched_content.content['title'], 'foo course')

    def test_course_unit_lesson_creation_and_query(self):
        """
        create a course, then unit, then lesson and make sure the entity
        relationships are all valid
        """
        course_key = Curriculum(
            content_type = 'course',
            content={'title':'numero uno'},
            ).put()
        unit_key = Curriculum(
            content_type = 'unit', 
            content={'course':int(course_key.id())}
            ).put()
        lesson_key = Curriculum(
            content_type = 'lesson',
            content={'course':int(course_key.id()), 'unit':int(unit_key.id())}
            ).put()

        lesson = lesson_key.get()
        unit = ndb.Key(Curriculum, lesson.content['unit']).get()
        course = ndb.Key(Curriculum, unit.content['course']).get()
        self.assertIsNotNone(unit)
        self.assertIsNotNone(course)
        self.assertEqual(course.content['title'], 'numero uno')

        