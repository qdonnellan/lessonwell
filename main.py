import webapp2
from views.public.front_page import FrontPage
from views.public.about_page import AboutPage
from views.public.sign_up_page import SignUpPage
from views.public.link_google_account_page import LinkGoogleAccountPage
from views.teacher.success_page import SuccessPage
from api.request_handlers.content_api import ContentAPI
from api.request_handlers.validate_username_api import ValidateUsernameAPI

app = webapp2.WSGIApplication([
    ('/api/content/(\w+)', ContentAPI), 
    ('/api/content/(\w+)/(\w+)', ContentAPI), 
    ('/api/content/(\w+)/(\w+)/(\w+)', ContentAPI),
    ('/api/content/(\w+)/(\w+)/(\w+)/(\w+)', ContentAPI),
    ('/api/validate_username/(\w+)', ValidateUsernameAPI),
    ('/success', SuccessPage),
    ('/about', AboutPage),
    ('/sign_up', SignUpPage),
    ('/link', LinkGoogleAccountPage), 
    ('.*', FrontPage),
    ],debug=False)
