from flask import Flask
from flask.ext.restful import Api
from views.public.front import FrontPage
from views.public.link import LinkPage
from views.public.signup import SignUpPage
from views.public.success import SuccessPage
from views.public.sandbox import SandboxPage
from views.teacher.profile import ProfilePage
from views.teacher.edit_content import EditContentPage
from api.users import UsersAPI
from api.card import CardAPI
from api.curriculum import CurriculumAPI
from api.customer import CustomerAPI

app = Flask(__name__)
rest_api = Api(app)

# the main application routes
app.add_url_rule('/', view_func=FrontPage.as_view('front'))
app.add_url_rule('/link', view_func=LinkPage.as_view('link'))
app.add_url_rule('/signup', view_func=SignUpPage.as_view('signup'))
app.add_url_rule('/success', view_func=SuccessPage.as_view('success'))
app.add_url_rule('/edit', view_func=EditContentPage.as_view('edit'))
app.add_url_rule('/sandbox', view_func=SandboxPage.as_view('sandbox'))
app.add_url_rule('/<username>', view_func=ProfilePage.as_view('profile'))

# the restful API routes
rest_api.add_resource(
    UsersAPI, 
    '/api/users', 
    '/api/users/<user_id>'
    )

rest_api.add_resource(
    CurriculumAPI, 
    '/api/curriculum',
    '/api/curriculum/<content_id>'
    )

rest_api.add_resource(
    CardAPI, 
    '/api/card')

rest_api.add_resource(
    CustomerAPI, 
    '/api/customer'
    )

