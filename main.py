import webapp2
from views.public.front_page import FrontPage
from views.public.about_page import AboutPage
from views.public.sign_up_page import SignUpPage
from views.public.link_google_account_page import LinkGoogleAccountPage
from api.request_handlers.content_api import ContentAPI

app = webapp2.WSGIApplication([
    ('/api/content/(\w+)', ContentAPI), 
    ('/api/content/(\w+)/(\w+)', ContentAPI), 
    ('/api/content/(\w+)/(\w+)/(\w+)', ContentAPI),
    ('/api/content/(\w+)/(\w+)/(\w+)/(\w+)', ContentAPI),
    ('/about', AboutPage),
    ('/sign_up', SignUpPage),
    ('/link', LinkGoogleAccountPage), 
    ('.*', FrontPage),
    ],debug=False)
