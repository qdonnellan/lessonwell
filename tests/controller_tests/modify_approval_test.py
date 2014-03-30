from tests.main_test_handler import TestBase
from controllers.modify_approval import new_approval_request, update_approval
from models.curriculum import Curriculum 
from controllers.fetch_curriculum import get_course_by_id
from controllers.new_course import new_course

class ModifyApprovalTest(TestBase):
    """
    test the implementation of the controllers which create 
    and modify approval
    """
    def create_new_approval(self):
        """
        a helper class for quickly creating a new approval item
        """
        teacher = self.create_and_return_local_user()
        course_id = new_course({
            'teacher' : teacher.key.id(),
            'title' : 'foo course',
            'body' : 'hey look mom',
            })
        new_approval_request(
            course = get_course_by_id(course_id), 
            googleID='123', 
            formalName='John Doe', 
            email='j@example.com')

    def test_new_approval_request(self):
        """
        create a new approval and assert that it shows up in the database
        """
        self.create_new_approval()
        course = Curriculum.query().get()
        self.assertIn('123', course.content['pending_approval'])





