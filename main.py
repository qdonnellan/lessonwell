import webapp2
from views.public.front_page import FrontPage
from views.public.about_page import AboutPage
from views.public.sign_up_page import SignUpPage
from views.public.sandbox import Sandbox
from views.public.link_google_account_page import LinkGoogleAccountPage
from views.teacher.success_page import SuccessPage
from views.teacher.profile_page import ProfilePage
from views.teacher.edit_content import EditContent
from api.request_handlers.curriculum_api import CurriculumAPI
from api.request_handlers.validate_username_api import ValidateUsernameAPI
from api.request_handlers.user_api import UserAPI

app = webapp2.WSGIApplication([
    ('/api/course/(\w+)', CurriculumAPI), 
    ('/api/validate_username/(\w+)', ValidateUsernameAPI),
    ('/api/user/(\w+)', UserAPI),
    ('/success', SuccessPage),
    ('/sandbox', Sandbox),
    ('/about', AboutPage),
    ('/sign_up', SignUpPage),
    ('/link', LinkGoogleAccountPage), 
    ('/edit', EditContent),
    ('/(\w+)', ProfilePage),
    ('.*', FrontPage),
    ],debug=False)
