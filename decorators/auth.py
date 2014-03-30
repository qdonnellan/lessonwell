from google.appengine.api import users
from controllers.fetch_curriculum import get_course_by_id
from controllers.fetch_user import get_user_by_google_id

def link_if_no_google_user(decorated_function):
    """
    if the current_user is not authenticated to this app, 
    redirect to the link page
    """
    def check_current_user(self, *kw, **kwargs):
        current_user = users.get_current_user()
        if not current_user:
            self.redirect('/link')
        else:
            decorated_function(self, *kw, **kwargs)
    return check_current_user

def abort_if_no_google_user(decorated_function):
    """
    if the current_user is not authenticated to this app, 
    abort with a 401 error
    """
    def check_current_user(self, *kw, **kwargs):
        current_user = users.get_current_user()
        if not current_user:
            self.abort(401)
        else:
            decorated_function(self, *kw, **kwargs)
    return check_current_user

def local_user_required(decorated_function):
    """
    if no local user is present, the request is aborted
    """
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
    """
    check if the current user is approved to view this course/unit/lesson

    courseID should be the first kw, kw[0]
    """
    def approve_or_deny(self,*kw,**kwargs):
        try:
            contentID = kw[0]
            course = get_course_by_id(contentID)
            if course.content['private']:
                googleID = str(user.get_current_user().user_id())
                if googleID not in course.content['approved_students']:
                    raise Exception('not approved to view this course')
        except Exception as e:
            self.write_json({'error': str(e)})
        else:
            decorated_function(self, *kw, **kwargs)
    return approve_or_deny
