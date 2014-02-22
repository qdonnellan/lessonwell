from google.appengine.ext import ndb

class HelpDocs(ndb.Model):
    '''
    help documentation for the website, edited by users
    '''
    title = ndb.StringProperty(required = True)
    body = ndb.TextProperty(required = False)
    category = ndb.StringProperty(required = True)