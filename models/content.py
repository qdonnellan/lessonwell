from google.appengine.ext import ndb

class Content(ndb.Model):
    '''
    content is either a course, unit or Lesson

    Lessons have Unit parents, Units have Course parents, Courses have appUser parents
    '''
    
    title = ndb.StringProperty(required = True)
    body = ndb.TextProperty(required = False)
    contentType = ndb.StringProperty(required = True)
    image = ndb.StringProperty(required = False)
    active = ndb.TextProperty(required = False)
    last_modified = ndb.DateTimeProperty(auto_now = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    privacy = ndb.StringProperty(required = False)
    listed = ndb.StringProperty(required=False)
    access_amount = ndb.IntegerProperty(required = False)
    passphrase = ndb.StringProperty(required=False)
    standards = ndb.StringProperty(required = False)
    popularity = ndb.IntegerProperty(required=False, default = 0)
    blobs = ndb.JsonProperty(required=False)