from tests.main_test_handler import TestBase
from controllers.modify_approval import new_approval_request
from controllers.fetch_curriculum import get_course_by_id
from controllers.new_course import new_course
from google.appengine.ext import ndb
from models.curriculum import Curriculum

class FetchApprovalTest(TestBase):
    """
    test the implementation of the controllers which fetch approvals
    """
    def create_several_approvals_for_course(self, number_of_courses = 1):
        """
        create a course then approve several googleID's to access the course

        a helper method for the tests in this class; returns the course for 
        which the approvals were generated. If more than 1 course is created, 
        return the user instead of course/ids
        """
        teacher = self.create_and_return_local_user()
        for N in range(number_of_courses):
            course_id = new_course({
                'teacher' : teacher.key.id(),
                'title' : 'foo course',
                'body' : 'hey look mom',
                })
            list_of_ids_to_approve = [1,2,3,4,5]
            course = get_course_by_id(course_id)
            for i in list_of_ids_to_approve:
                new_approval_request(
                    course = course, 
                    googleID=i, 
                    formalName='John Doe %s' % i, 
                    email='j%s@example.com' % i
                    )
        
    def test_get_approved_users(self):
        """
        create a course, add a few approval requests, 
        and assert that they are retrieved correctly
        """
        self.create_several_approvals_for_course(1)
        course = Curriculum.query().get()
        self.assertEqual(
            course.content['pending_approval'], 
            [1,2,3,4,5],
            )




        


