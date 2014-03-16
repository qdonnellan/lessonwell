from tests.main_test_handler import TestBase
import unittest

class ProfileViewTest(TestBase):
    '''
    test that the profile views are implemented and functioning correctly
    '''

    def test_public_profile_page_view(self):
        '''
        test public view of a profile page of a known user
        '''
        self.create_and_return_local_user(username='testuser')
        response = self.testapp.get('/testuser')
        self.assertEqual(response.status_int, 200)





