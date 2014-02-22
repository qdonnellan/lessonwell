from models.approval import Approval
from fetch_content import get_all_content

def get_approved_users(course):
    '''
    get a list of approved users for this course
    '''
    if course is not None:
        users = Approval.query(ancestor = course.key).order(Approval.status)
        return users
    else:
        return []

def get_approval_status_for_google_id(course, googleID):
    '''
    check if this googleID is approved to view this course

    return the approval object if it exists, or None if it does not
    '''
    approval = Approval.query(Approval.googleID == str(googleID), ancestor = course.key).get()
    return approval

def get_all_approval_requests(author):
    '''
    detect the pending approval requests for all courses authored by author

    returns a list of pending approval requests
    '''
    detection = []
    allCourses = get_all_content(author.key, "course")
    for course in allCourses:
        users = get_approved_users(course)
        for user in users:
            if user.status == 'pending':
                detection.append(course.key.id())
    if detection == []:
        detection = None
    return detection

