from tests.main_test_handler import TestBase

class SignUpSuccessPageTest(TestBase):
    '''
    test that the sign up success page is working correctly
    '''

    def test_success_page_view_not_authenticated(self):
        '''
        test views of '/success' with a not authorized user
        '''
        response = self.testapp.get('/success', status = 401)
        self.assertEqual(response.status_int, 401)

    def test_success_page_view_with_authorized_user(self):
        '''
        test views of '/success' with an authorized user
        '''
        self.create_google_user(user_id = '123')
        user = self.create_and_return_local_user(googleID = '123')
        response = self.testapp.get('/success')
        self.assertEqual(response.status_int, 200)

    