from views.main_view_handler import ViewHandler
from controllers.fetch_user import get_user_by_username

class ProfilePage(ViewHandler):
    '''
    the request handler for the profile page
    '''
    
    def get(self, username):
        '''
        handle the get request for the profile page
        '''
        teacher = get_user_by_username(username)
        self.render(
            'profile.html', 
            teacher = teacher,
            )