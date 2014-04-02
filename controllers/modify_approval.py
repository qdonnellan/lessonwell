def new_approval_request(course, googleID, formalName, email):
    """
    process the supposedly new approval of the googleID for ths course

    if approval instance already exists, do nothing
    """
    googleID = int(googleID)
    if googleID not in course.content['approved_students']:
        if googleID not in course.content['pending_approval']:
            course.content['pending_approval'].append(googleID)
            course.put()

def update_approval(course, googleID, status):
    """
    update the approval status for a particular googleID for a course
    """
    googleID = int(googleID)
    if status == 'delete':
        if googleID in course.content['approved_students']:
            course.content['approved_students'].remove(googleID)
            course.put()
        elif googleID in course['content']['pending_approval']:
            course.content['pending_approval'].remove(googleID)
            couse.put()


    elif status == 'approve':
        if googleID not in course['content']['approved_students']:
            course.content['approved_students'].append(googleID)
            course.put()
        if googleID in course.content['pending_approval']:
            course.content['pending_approval'].remove(googleID)
            course.put()
