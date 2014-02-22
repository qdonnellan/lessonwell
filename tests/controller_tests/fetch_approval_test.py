from tests.main_test_handler import TestBase
from controllers.fetch_approval import get_approved_users, get_approval_status_for_google_id, get_all_approval_requests
from controllers.modify_approval import new_approval_request

from google.appengine.ext import ndb
from models.content import Content

class FetchApprovalTest(TestBase):
    '''
    test the implementation of the controllers which fetch approvals
    '''
    def create_several_approvals_for_course(self, number_of_courses = 1):
        '''
        create a course then approve several googleID's to access the course

        a helper method for the tests in this class; returns the course for which the
        approvals were generated. If more than 1 course is created, return the user instead of course/ids
        '''
        user = self.create_and_return_local_user()
        for N in range(number_of_courses):
            course_id = self.create_sample_course(user=user)
            course = ndb.Key(Content, int(course_id), parent=user.key).get()
            list_of_ids_to_approve = ['1', '2', '3', '4', '5']
            for i in list_of_ids_to_approve:
                new_approval_request(course, googleID=i, formalName='John Doe %s' % i, email='j%s@example.com' % i)
        if number_of_courses > 1:
            return user
        else:
            return course, list_of_ids_to_approve
        
    def test_get_approved_users(self):
        '''
        create a course, add a few approval requests, and assert that they are retrieved correctly
        '''
        course, list_of_ids = self.create_several_approvals_for_course()
        approved_users = get_approved_users(course = course)
        self.assertEqual(len(approved_users.fetch()), len(list_of_ids))

    def test_get_approval_status_for_google_id(self):
        '''
        create a course, add a few approval requests, check that one of them is on the list

        also check that a user not approved isn't somehow in the list of approvals
        '''
        course, list_of_ids = self.create_several_approvals_for_course()
        approval_status = get_approval_status_for_google_id(course=course, googleID = '1').status
        self.assertEqual(approval_status, 'pending')
        self.assertIsNone(get_approval_status_for_google_id(course=course, googleID = '999'))

    def test_get_all_approvals_for_author(self):
        '''
        create multiple courses with many approvals each, then fetch all of them
        '''
        user = self.create_several_approvals_for_course(number_of_courses=3)
        all_approval_requests = get_all_approval_requests(user)
        self.assertEqual(len(all_approval_requests), 15)



        


