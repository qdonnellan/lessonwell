from google.appengine.ext import ndb

class Content(ndb.Model):
    """
    content is either a course, unit or lesson
    """
    title = ndb.StringProperty(required = True)
    body = ndb.TextProperty(required = False)
    contentType = ndb.StringProperty(required = True)
    active = ndb.TextProperty(required = False)
    last_modified = ndb.DateTimeProperty(auto_now = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    privacy = ndb.StringProperty(required = False)
    listed = ndb.StringProperty(required=False)
    passphrase = ndb.StringProperty(required=False)
    blobs = ndb.JsonProperty(required=False)
