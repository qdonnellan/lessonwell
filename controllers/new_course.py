from fetch_user import get_user
from models.curriculum import Curriculum

def new_course(content):
    """
    create a new course entity; return the id of the new course

    content should conform to:
    content = {
        'teacher' : (str or int, Required),
        'title' : (string),
        'body' : (string),
        'private' : (boolean),
    }
    """
    teacher_id = content['teacher']
    teacher = get_user(teacher_id)
    if teacher is None:
        raise Exception("invalid user id: that user does not exist")

    if 'title' not in content:
        content['title'] = ''
    if 'body' not in content:
        content['body'] = ''
    
    if 'private' not in content or content['private'] != True:
        content['private'] = False
        
    content['approved_students'] = []
    content['pending_approval'] = []
    content['units'] = []
    content['listed'] = False
    key = Curriculum(content_type = 'course', content = content).put()

    if teacher.courses:
        teacher.courses.append(int(key.id()))
    else:
        teacher.courses = [int(key.id())]
    teacher.put()

    return int(key.id())


