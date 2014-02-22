from models.approval import Approval
from fetch_approval import get_approval_status_for_google_id

def new_approval_request(course, googleID, formalName, email):
    '''
    process the supposedly new approval of the googleID for ths course

    if approval instance already exists, do nothing
    '''
    existing_approval = get_approval_status_for_google_id(course, googleID)
    if existing_approval is None:
        approvalObject = Approval(
            googleID = googleID,
            formalName = formalName, 
            status = 'pending', 
            parent = course.key,
            email = email
            )
        approvalObject.put()

def update_approval(course, googleID, status):
    '''
    update the approval status for a particular googleID for a course
    '''
    current_approval = get_approval_status_for_google_id(course, googleID)
    if status == 'delete':
        current_approval.key.delete()
    else:
        current_approval.status = status
        current_approval.put()