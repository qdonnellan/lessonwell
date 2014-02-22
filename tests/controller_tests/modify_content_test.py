from tests.main_test_handler import TestBase
from controllers.modify_content import new_content, edit_content

from models.content import Content

class ModifyContentTest(TestBase):
    '''
    test the modify content controller functions
    '''

    def test_new_content_controller(self):
        '''
        test that the new content controller is working correctly
        '''
        local_user = self.create_and_return_local_user()
        new_content(
            title = 'Foo',
            body = 'A lesson on bar',
            parentKEY = local_user.key,
            contentType = 'course',
            privacy = 'public',
            listed = None
            )
        self.assertEqual(Content.query().count(),1)

    def test_edit_content_controller(self):
        '''
        test the edit content controller is working fine
        '''
        local_user = self.create_and_return_local_user()
        content_id = new_content(
            title = 'Foo',
            body = 'A lesson on bar',
            parentKEY = local_user.key,
            contentType = 'course',
            privacy = 'public',
            listed = None
            )
        self.assertEqual(Content.query().count(),1)
        edit_content(contentID = content_id, parentKEY = local_user.key, title="NewFoo")
        



