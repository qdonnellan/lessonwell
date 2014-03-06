from tests.main_test_handler import TestBase
import json

class GetUserAPITest(TestBase):
    '''
    test the implementation of the user api
    '''

    def test_simple_user_fetch(self):
        '''
        fetch a known user with an api get request
        '''
        user = self.create_and_return_local_user(username='foouser')
        user_id = user.key.id()
        response = self.testapp.get('/api/user/%s' % user_id)
        json_user = json.loads(response.body)
        self.assertEqual(json_user['username'], 'foouser')

    def test_user_fetch_for_not_existing_user(self):
        '''
        fetch a user that is known to not exist
        '''
        response = self.testapp.get('/api/user/9999999')
        json_user = json.loads(response.body)
        self.assertEqual(json_user['error'], 'that user does not exist')

        



