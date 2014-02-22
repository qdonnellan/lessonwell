from tests.main_test_handler import TestBase
from models.content import Content
import unittest
from google.appengine.ext.db import BadValueError

class ContentModelTest(TestBase):
    '''
    test the implementation of the content model 
    '''

    def test_simple_creation_of_new_content_model(self):
        '''
        test a simple put() of a new content model 
        '''
        new_content = Content()
        new_content.populate(
            title = 'foo',
            contentType = 'course'
            )
        new_content.put()
        self.assertIsNotNone(new_content.created)