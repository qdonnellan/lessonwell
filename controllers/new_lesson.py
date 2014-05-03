from fetch_user import get_user
from models.curriculum import Curriculum
from fetch_curriculum import get_content_by_id

def new_lesson(content):
    """
    create a new lesson and return the lesson id
    """
    unit_id = content['unit']
    unit = get_content_by_id(unit_id)
    if unit is None:
        raise Exception("invalid unit id: that unit does not exist")

    if 'title' not in content:
        content['title'] = ''
    if 'body' not in content:
        content['body'] = ''

    content['private'] = unit.content['private']
    content['teacher'] = unit.content['teacher']
    content['course'] = unit.content['course']

    key = Curriculum(content_type = 'lesson', content = content).put()
    
    # add this lesson to the parent unit's lesson list
    unit.content['lessons'].append(int(key.id()))
    unit.put()

    return int(key.id())