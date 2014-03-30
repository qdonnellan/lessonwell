from tests.main_test_handler import TestBase
from google.appengine.ext import ndb
from controllers.new_course import new_course

from models.curriculum import Curriculum 

class NewCourseTest(TestBase):
    """
    test the implementation of the new course function
    """

    def test_new_course_controller(self):
        """
        test that the new course controller is working property
        """
        local_user = self.create_and_return_local_user()
        content = {
            'teacher' : int(local_user.key.id()),
            'title' : 'foo course',
            'body' : 'study hard, learn well, duh',
        }
        course_id = new_course(content)
        fetched_course = ndb.Key('Curriculum', course_id).get()
        self.assertEqual(fetched_course.content['title'], 'foo course')

    def test_new_course_with_bad_user_id(self):
        """
        attempt to create a course with a bad user id should raise an exception
        """
        content = {
            'title' : 'foo course', 
            'body' : 'this course has no owner', 
            'teacher' : 99999999
            }
        self.assertRaises(Exception, new_course, content)

        # let's also make sure the error message was passed!
        try: 
            new_course(content)
        except Exception as e:
            self.assertIn("that user does not exist", str(e))

    def test_new_course_with_no_user_id_passed(self):
        """
        attempt to create a course with no teacher id passed
        """
        content = {'title':'foo', 'body':'bar'}
        self.assertRaises(KeyError, new_course, content)

    def test_new_course_with_base_content(self):
        """
        attmept to create a course with bad content information
        
        content should be a JSON serializable dict!
        """
        self.assertRaises(Exception, new_course, 'badfas')



        
        


