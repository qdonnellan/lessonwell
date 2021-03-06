from flask import Flask
from flask.ext.restful import Api
from views.public.front import FrontPage
from views.public.google_page import GooglePage
from views.public.link import LinkPage
from views.migrate import MigratePage
from views.public.about import AboutPage, PrivacyPage, TermsPage
from views.public.signup import SignUpPage
from views.public.success import SuccessPage
from views.public.sandbox import SandboxPage
from views.public.sponsor import SponsorPage
from views.public.pricing import PricingPage
from views.landing_pages.teacher import LandingPage1
from views.public.administrator import AdministratorPage
from views.teacher.profile import ProfilePage
from views.teacher.edit_content import EditContentPage
from api.users import UsersAPI
from api.card import CardAPI
from api.curriculum import CurriculumAPI
from api.customer import CustomerAPI
from api.redeem import RedeemAPI

app = Flask(__name__)
rest_api = Api(app)



# the main application routes
app.add_url_rule('/', view_func=FrontPage.as_view('front'))
app.add_url_rule('/link', view_func=LinkPage.as_view('link'))
app.add_url_rule('/about', view_func=AboutPage.as_view('about'))
app.add_url_rule('/signup', view_func=SignUpPage.as_view('signup'))
app.add_url_rule('/privacy', view_func=PrivacyPage.as_view('privacy'))
app.add_url_rule('/terms', view_func=TermsPage.as_view('terms'))
app.add_url_rule('/success', view_func=SuccessPage.as_view('success'))
app.add_url_rule('/edit', view_func=EditContentPage.as_view('edit'))
app.add_url_rule('/sandbox', view_func=SandboxPage.as_view('sandbox'))
app.add_url_rule('/google', view_func=GooglePage.as_view('google_page'))
app.add_url_rule('/administrator', view_func=AdministratorPage.as_view('administrator'))
app.add_url_rule('/sponsor/<username>', view_func=SponsorPage.as_view('sponsor'))
app.add_url_rule('/pricing/<pricing_type>', view_func=PricingPage.as_view('pricing'))
app.add_url_rule('/pricing', view_func=PricingPage.as_view('pricing_main'))
app.add_url_rule('/<username>', view_func=ProfilePage.as_view('profile'))

# Some landing pages

app.add_url_rule('/stop_wasting_time', view_func=LandingPage1.as_view('stop_wasting_time'))

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

rest_api.add_resource(
    RedeemAPI, 
    '/api/redeem'
    )

