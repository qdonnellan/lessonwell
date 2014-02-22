from tests.main_test_handler import TestBase

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


