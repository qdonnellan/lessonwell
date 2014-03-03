from tests.main_test_handler import TestBase
import unittest

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

    def test_public_link_google_account_page(self):
        '''
        test views of '/link'
        '''
        response = self.testapp.get('/link')
        self.assertEqual(response.status_int, 200)

    def test_public_sandbox_page(self):
        '''
        the sandbox page should be up and running
        '''
        response = self.testapp.get('/sandbox')
        self.assertEqual(response.status_int, 200)




