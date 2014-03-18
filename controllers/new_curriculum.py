from google.appengine.ext import ndb
from models.curriculum import Curriculum

def new_course(content):
    """
    create a new course entity; return the id of the new course
    """
    teacher_id = content['teacher']
    teacher = ndb.Key('User', teacher_id).get()
    if teacher is None:
        raise Exception("invalid user id: that user does not exist")

    if 'title' not in content:
        content['title'] = ''
    if 'body' not in content:
        content['body'] = ''
    
    content['private'] = False
    content['students'] = []
    content['units'] = []
    content['passphrase'] = ''
    content['listed'] = False
    key = Curriculum(content_type = 'course', content = content).put()
    return int(key.id())







