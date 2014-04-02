from google.appengine.ext import ndb

def get_content_by_id(content_id):
    """
    return the curriculum object or None if it doesn't exist
    """
    content = ndb.Key('Curriculum', int(content_id)).get()
    return content

def get_course_by_id(content_id):
    """
    return the course associated with the content_id

    the content_id may be for a lesson, unit, or course
    """
    content = ndb.Key('Curriculum', int(content_id)).get()
    if not content:
        raise Exception("that content id does not exist")
        
    if content.content_type =='course':
        return content
    else:
        course_id = content.content['course']
        course = ndb.Key('Curriculum', int(course_id)).get()
        return course
