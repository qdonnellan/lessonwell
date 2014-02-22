from google.appengine.ext import ndb

class Approval(ndb.Model):
    '''
    specify which googleID's are approved to access which course

    approval entities have parents which are course objects
    '''
    googleID = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = True)
    formalName = ndb.StringProperty(required = True)
    status = ndb.StringProperty(required = True)