from views.main_view_handler import ViewHandler

class FrontPage(ViewHandler):
    def get(self):
        self.render('front.html', homeActive = 'active')