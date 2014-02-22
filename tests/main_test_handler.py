import unittest
import webtest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from controllers.modify_user import new_user
from controllers.fetch_user import get_user_by_username
from controllers.modify_content import new_content

import main

class TestBase(unittest.TestCase):
    '''
    a useful class that other tests can inherit
    '''

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()
        self.testbed.init_datastore_v3_stub()  
        self.testapp = webtest.TestApp(main.app)

    def tearDown(self):
        self.testbed.deactivate()

    def create_google_user(self, email_address, admin=False, user_id = '123'):
        self.testbed.setup_env(
            USER_EMAIL = email_address,
            USER_ID = user_id,
            USER_IS_ADMIN = '1' if admin else '0',
            overwrite = True
        )

    def create_and_return_local_user(self, username='testuser123'):
        '''
        create a user with a default email address and formal name, return that object

        a helper function for tests that require a local (app) user to operate
        '''
        new_user(username = username, email='test@example.com', formalName ='James Smith', googleID = '123')
        return get_user_by_username(username)

    def create_sample_course(self, title='foo', body='bar', user = None):
        if not user:
            user = self.create_and_return_local_user()
        content_id = new_content(title=title, body=body, parentKEY=user.key, contentType='course', privacy=None, listed=None)
        return content_id




