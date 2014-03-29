from views.main_view_handler import ViewHandler
from decorators.auth import local_user_required

class EditContent(ViewHandler):
    """
    the request handler for the edit content page
    """
    
    @local_user_required
    def get(self):
        """
        handle the get request for the edit content page
        """
        self.render('edit.html')