from tests.main_test_handler import TestBase
from models.content import Content 
from models.user import User

from controllers.fetch_content_by_id import get_course, get_unit, get_lesson, get_content

class FetchContentByIDTest(TestBase):
    '''
    this tests the easy fetch controllers which return content based on ids
    '''

    def create_user_return_user_and_id(self):
        user = User(username='foo',email='bar',googleID='123').put()
        return user.get(), user.id()

    def create_content_return_content_and_id(self, parent, contentType):
        content = Content(title='bla', contentType=contentType, parent=parent.key).put()
        return content.get(), content.id()

    def test_get_course(self):
        '''
        get a course given a userID and courseID
        '''
        user, userID = self.create_user_return_user_and_id()
        course, courseID = self.create_content_return_content_and_id(user, 'course')
        self.assertIsNotNone(get_course(userID=userID, courseID=courseID))

    def test_get_unit(self):
        '''
        get a unit given userID, courseID, and unitID
        '''
        user, userID = self.create_user_return_user_and_id()
        course, courseID = self.create_content_return_content_and_id(user, 'course')
        unit, unitID = self.create_content_return_content_and_id(course, 'unit')
        self.assertIsNotNone(get_unit(userID=userID, courseID=courseID, unitID = unitID))

    def test_get_lesson(self):
        '''
        get a lesson given userID, courseID, unitID, and lessonID
        '''
        user, userID = self.create_user_return_user_and_id()
        course, courseID = self.create_content_return_content_and_id(user, 'course')
        unit, unitID = self.create_content_return_content_and_id(course, 'unit')
        lesson, lessonID = self.create_content_return_content_and_id(unit, 'lesson')
        self.assertIsNotNone(get_lesson(userID=userID, courseID=courseID, unitID = unitID, lessonID = lessonID))

    def get_content(self):
        '''
        the get_content controller will detect which params are passed and return the appropriate
        object by calling one of get_course, get_unit, or get_lesson
        '''
        user, userID = self.create_user_return_user_and_id()
        course, courseID = self.create_content_return_content_and_id(user, 'course')
        unit, unitID = self.create_content_return_content_and_id(course, 'unit')
        lesson, lessonID = self.create_content_return_content_and_id(unit, 'lesson')
        # no params means no content
        self.assertIsNone(get_content())
        # pass params distinct to a lesson
        self.assertEqual(get_content(userID, courseID, unitID, lessonID).contentType, 'lesson')
        # pass params distinct to a unit
        self.assertEqual(get_content(userID, courseID, unitID).contentType, 'unit')
        # pass params distinct to a course
        self.assertEqual(get_content(userID, courseID).contentType, 'course')



