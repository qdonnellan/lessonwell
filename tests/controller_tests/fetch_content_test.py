from tests.main_test_handler import TestBase
from controllers.fetch_content import get_content, get_all_content, get_all_courses

class FetchContentTest(TestBase):
    '''
    test the implementaiton of the controllers which fetch content
    '''

    def test_get_content(self):
        '''
        test the simple get_content controller
        '''
        user = self.create_and_return_local_user()
        course_id = self.create_sample_course(title = 'Foo Course', user=user)
        course_object = get_content(contentID = course_id, parentKEY = user.key)
        self.assertEqual(course_object.title, 'Foo Course')

    def test_get_all_content(self):
        '''
        create N courses and assert that get_all_content returns them all
        '''
        user = self.create_and_return_local_user()
        for i in range(10):
            self.create_sample_course(title = 'Foo Course %s' % i, user=user)
        content_query = get_all_content(parentKEY = user.key, contentType = 'course')
        self.assertEqual(content_query.count(), 10)

    def test_get_all_courses(self):
        '''
        create N course and assert that get_all_courses returns them all
        '''
        user = self.create_and_return_local_user()
        for i in range(10):
            self.create_sample_course(title = 'Foo Course %s' % i, user=user)
        content_query = get_all_courses()
        self.assertEqual(content_query.count(), 10)







