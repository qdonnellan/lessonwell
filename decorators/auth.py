from google.appengine.api import users
from controllers.fetch_content_by_id import get_course
from controllers.check_privacy import check_privacy
from controllers.fetch_approval import get_approval_status_for_google_id
from controllers.fetch_user import get_user_by_google_id

def link_if_no_google_user(decorated_function):
    '''
    if the current_user is not authenticated to this app, redirect to the link page
    '''
    def check_current_user(self, *kw, **kwargs):
        current_user = users.get_current_user()
        if not current_user:
            self.redirect('/link')
        else:
            decorated_function(self, *kw, **kwargs)
    return check_current_user

def abort_if_no_google_user(decorated_function):
    '''
    if the current_user is not authenticated to this app, abort with a 401 error
    '''
    def check_current_user(self, *kw, **kwargs):
        current_user = users.get_current_user()
        if not current_user:
            self.abort(401)
        else:
            decorated_function(self, *kw, **kwargs)
    return check_current_user

def local_user_required(decorated_function):
    '''
    if no local user is present, the request is aborted
    '''
    def check_for_local_user(self, *kw, **kwargs):
        try:
            current_user = users.get_current_user()
            user = get_user_by_google_id(current_user.user_id())
            if not user:
                raise Exception
        except:
            self.abort(401)
        else:
            decorated_function(self, *kw, **kwargs)
    return check_for_local_user

def check_approval(decorated_function):
    '''
    check if the current user is approved to view this course/unit/lesson

    userID should be the first kw, kw[0]
    courseID should be the second kw, kw[1]
    '''
    def approve_or_deny(self,*kw,**kwargs):
        userID, courseID = kw[0], kw[1]
        try:
            course = get_course(userID, courseID)
        except:
            self.write_json({'error':'that content does not exist'})
        else:
            is_private = check_privacy(course)
            if is_private:
                try:
                    current_user = users.get_current_user()
                    status = get_approval_status_for_google_id(course, current_user.user_id()).status
                    if status != 'approved': raise NameError('not approved')
                    decorated_function(self, *kw, **kwargs)
                except:
                    self.abort(401)
            else:
                decorated_function(self, *kw, **kwargs)
    return approve_or_deny
