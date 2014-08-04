from fetch_user import get_user, get_active_user
from models.curriculum import Curriculum
from controllers.fetch_curriculum import get_content_by_id

def modify_content(modified_content, content_id):
    """
    edit existing content, return the id of that content object
    """
    content_object = get_content_by_id(content_id)
    if 'title' in modified_content:
        content_object.content['title'] = modified_content['title']

    if 'body' in modified_content:
        content_object.content['body'] = modified_content['body']

    content_object.put()
    return content_id

def delete_content(content_id):
    """
    delete the content if possible
    """
    active_user = get_active_user()
    if not active_user:
        raise NameError("You are unauthorized to perform this action")
    else:
        content_object = get_content_by_id(content_id)
        content_type = content_object.content_type
        if int(content_object.content['teacher']) == int(active_user.key.id()):
            if content_type == 'course':
                active_user.courses.remove(int(content_object.key.id()))
                active_user.put()
            elif content_type == 'unit':
                course_id = content_object.content['course']
                parent_course = get_content_by_id(course_id)
                parent_course.content['units'].remove(int(content_object.key.id()))
                parent_course.put()
            elif content_type == 'lesson':
                unit_id = content_object.content['unit']
                parent_unit = get_content_by_id(course_id)
                parent_unit.content['lessons'].remove(int(content_object.key.id()))
                parent_unit.put()

            content_object.key.delete()

    
