from google.appengine.api import users

def google_user_required(decorated_function):
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

