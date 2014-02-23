from google.appengine.ext import ndb
from models.content import Content
from fetch_user import get_user

def get_content(userID = None, courseID = None, unitID = None, lessonID = None):
    '''
    determines which params were passed, then fetches that content
    '''
    if userID and courseID and not (unitID and lessonID):
        return get_course(userID, courseID)
    elif userID and courseID and unitID and not lessonID:
        return get_unit(userID, courseID, unitID)
    elif userID and courseID and unitID and lessonID:
        return get_lesson(userID, courseID, unitID, lessonID)
    else:
        return None

def get_course(userID, courseID):
    '''
    return a course given a userID and a courseID
    '''
    user = get_user(userID)
    course = ndb.Key(Content, int(courseID), parent=user.key).get()
    return course

def get_unit(userID, courseID, unitID):
    '''
    return a unit given a userID, courseID, and unitID
    '''
    course = get_course(userID, courseID)
    unit = ndb.Key(Content, int(unitID), parent=course.key).get()
    return unit

def get_lesson(userID, courseID, unitID, lessonID):
    '''
    return a lesson given a userID, courseID, unitID, and lessonID
    '''
    unit = get_unit(userID, courseID, unitID)
    lesson = ndb.Key(Content, int(lessonID), parent= unit.key).get()
    return lesson