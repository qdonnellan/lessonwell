from fetch_user import get_user
from models.curriculum import Curriculum
from fetch_curriculum import get_content_by_id

def new_unit(content):
    """
    create a new unit entity; return the id of the new unit
    """
    course_id = content['course']
    course = get_content_by_id(course_id)
    if course is None:
        raise Exception("invalid course id: that course does not exist")

    if 'title' not in content:
        content['title'] = ''
    if 'body' not in content:
        content['body'] = ''

    content['private'] = course.content['private']
    content['teacher'] = course.content['teacher']
    content['course'] = course_id
    content['lessons'] = []
    key = Curriculum(content_type = 'unit', content = content).put()

    # add this unit to the parent course's unit list
    course.content['units'].append(int(key.id()))
    course.put()

    return int(key.id())