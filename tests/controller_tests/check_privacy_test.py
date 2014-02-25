from tests.main_test_handler import TestBase
from controllers.check_privacy import check_privacy
from controllers.fetch_content_by_id import get_course

class CheckPrivacyTest(TestBase):
    '''
    test the implemenation of the handy controller "check_privacy"
    '''

    def test_check_privacy_of_public_course(self):
        '''
        a public course should not be private
        '''
        author = self.create_and_return_local_user()
        course_id = self.create_sample_course(user = author)
        course = get_course(author.key.id(), course_id)
        self.assertFalse(check_privacy(course))

    def test_check_privacy_of_privcate_course(self):
        '''
        a private course should be private
        '''
        author = self.create_and_return_local_user()
        course_id = self.create_sample_course(user = author, privacy = 'private')
        course = get_course(author.key.id(), course_id)
        self.assertTrue(check_privacy(course))

    def test_check_privacy_of_none_course(self):
        '''
        a privacy check on nothing should raise an exception
        '''
        self.assertRaises(Exception, check_privacy, None)

