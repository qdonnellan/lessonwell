from models.privacyMap import PrivacyMap

def approved_users(course):
    '''
    get a list of approved users for this course
    '''
    if course is not None:
        users = PrivacyMap.query(ancestor = course.key).order(PrivacyMap.status)
        return users
    else:
        return []

def googleID_approval(course, googleID):
    '''
    check if this googleID is approved to view this course

    return the approval object if it exists, or None if it does not
    '''
    approval = PrivacyMap.query(PrivacyMap.googleID == str(googleID), ancestor = course.key).get()
    return approval

def approval_request(course, googleID, formalName, status, email):
    '''
    process the supposedly new approval of the googleID for ths course

    if approval already exists, do nothing
    '''
    existing_approval = googleID_approval(course, googleID)
    if existing_approval is None or status == 'paid':
        approvalObject = PrivacyMap(
            googleID = googleID,
            formalName = formalName, 
            status = status, 
            parent = course.key,
            email = email
            )
        approvalObject.put()

def update_approval(course, googleID, status):
    '''
    update the approval status for a particular googleID for a course
    '''
    current_approval = googleID_approval(course, googleID)
    if status == 'delete':
        current_approval.key.delete()
    else:
        current_approval.populate(
            status = status)
        current_approval.put()

def detect_approval_requests(author):
    '''
    detect the pending approval requests for all courses authored by author

    returns a list of pending approval requests
    '''
    detection = []
    allCourses = getAllContent(author.key, "course")
    for course in allCourses:
        users = approved_users(course)
    for user in users:
        if user.status == 'pending':
            detection.append(course.key.id())
    if detection == []:
        detection = None
    return detection

