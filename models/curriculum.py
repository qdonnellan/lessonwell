from google.appengine.ext import ndb

class Curriculum(ndb.Model):
    """
    the new curriculum flat curriculum model
    """

    content_type = ndb.StringProperty(required = True)
    content = ndb.JsonProperty(required=False)

