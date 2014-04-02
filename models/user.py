from google.appengine.ext import ndb

class User(ndb.Model):
    '''
    the user class
    '''
    username = ndb.StringProperty(required = True)
    username_lower = ndb.ComputedProperty(lambda self: self.username.lower())
    googleID = ndb.StringProperty(required = True)
    formalName = ndb.StringProperty(required = False)
    email = ndb.StringProperty(required = True)
    bio = ndb.TextProperty(required=False)
    pic = ndb.StringProperty(required = False)
    tagline = ndb.StringProperty(required = False)
    stripeID = ndb.StringProperty(required = False)
    created = ndb.DateTimeProperty(auto_now_add = True)
    stripe_pub_key = ndb.StringProperty(required = False)
    stripe_access_token = ndb.StringProperty(required = False)
    courses = ndb.JsonProperty(required = False)