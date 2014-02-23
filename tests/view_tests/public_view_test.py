from tests.main_test_handler import TestBase
import unittest

@unittest.skip("skipping the PublicViewTest")
class PublicViewTest(TestBase):
    '''
    test that the public views are implemented and functioning correctly
    '''

    def test_public_front_page_view(self):
        '''
        test views of '.*', and '/'
        '''
        response = self.testapp.get('/')
        self.assertEqual(response.status_int, 200)

    def test_public_about_page_view(self):
        '''
        test views of '/about' and 'about/?doc=terms', 'about/?doc=privacy', etc.
        '''
        for page in ['/about', '/about/?doc=terms', '/about/?doc=privacy']:
            response = self.testapp.get('/about')
            self.assertEqual(response.status_int, 200)
            self.assertIn('About', response.body)

    def test_public_sign_up_page_view_not_authenticated(self):
        '''
        test views of '/sign_up'
        '''
        response = self.testapp.get('/sign_up')
        self.assertEqual(response.status_int, 302)

    def test_public_sign_up_page_view_with_google_authentication(self):
        '''
        test views of '/sign_up' with a user authenticated to google
        '''
        self.create_google_user()
        response = self.testapp.get('/sign_up')
        self.assertEqual(response.status_int, 200)

    def test_public_link_google_account_page(self):
        '''
        test views of '/link'
        '''
        response = self.testapp.get('/link')
        self.assertEqual(response.status_int, 200)




