from views.main_view_handler import ViewHandler

class FrontPage(ViewHandler):
    def get(self):
        self.render('home.html', homeActive = 'active')