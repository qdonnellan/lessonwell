from google.appengine.ext import ndb

class PrivacyMap(ndb.Model):
    '''
    specify the privacy connections between google users and content objects
    '''
    googleID = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = True)
    formalName = ndb.StringProperty(required = True)
    status = ndb.StringProperty(required = True)