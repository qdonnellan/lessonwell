from tests.main_test_handler import TestBase
from controllers.modify_approval import new_approval_request, update_approval
from models.approval import Approval
from models.content import Content
from google.appengine.ext import ndb

class ModifyApprovalTest(TestBase):
    '''
    test the implementation of the controllers which create and modify approval
    '''
    def create_and_return_new_approval(self):
        '''
        a helper class for quickly creating a new approval item
        '''
        user = self.create_and_return_local_user()
        course_id = self.create_sample_course(user=user)
        course = ndb.Key(Content, int(course_id), parent=user.key).get()
        new_approval_request(course, googleID='123', formalName='John Doe', email='j@example.com')
        return Approval.query().get()

    def test_new_approval_request(self):
        '''
        create a new approval and assert that it shows up in the database
        '''
        approval_instance = self.create_and_return_new_approval()
        self.assertEqual(approval_instance.googleID, '123')
        self.assertEqual(approval_instance.status, 'pending')

    def test_update_approval_request(self):
        '''
        create a new approval then edit it with the update_approval request

        changes should be reflected in the database
        '''
        old_approval = self.create_and_return_new_approval()
        course = old_approval.key.parent().get()
        update_approval(course = course, googleID = '123', status='approved')
        updated_approval = Approval.query().get()
        self.assertEqual(updated_approval.status, 'approved')

    def test_delete_approval_request(self):
        '''
        a deleted approval should be deleted from the database
        '''
        approval_instance = self.create_and_return_new_approval()
        course = approval_instance.key.parent().get()
        update_approval(course = course, googleID = '123', status='delete')
        self.assertEqual(Approval.query().count(), 0)




