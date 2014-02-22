import webapp2
from jinja_environment import JinjaEnvironment
from google.appengine.api import users

from stripe_keys import pub_key

class ViewHandler(webapp2.RequestHandler):
    '''
    MainHandler inherited by all views to make rendering views super easy
    '''

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
      
    def render_str(self, template, **params):
        environment = JinjaEnvironment().environment
        t = environment.get_template(template)
        return t.render(params)

    def render(self, template, **kw):  
        '''
        simply render a template with passed variables using Jinja2
        '''                
        self.write(self.render_str(
            template, 
            google_users_api = users,
            stripe_publish_key = pub_key,
            **kw
            )
        )

    def admin_required(self):
        '''
        handle admin authentication and pass the request if valid or abort ot stop code execution
        '''
        if not users.is_current_user_admin():
            self.abort(401)

    def user_required(self, specific_domain = None):
        '''
        handle user authentication and pass the request is valid or abort and stop code execution

        if "specific_domain" is passed, then restrict access to users who have email that matches 
        the specific_domain string. 

        For example: specific_domain = "@example.com" will only accept users authenticated to the 
        @example.com domain
        '''
        user = users.get_current_user()
        if user and specific_domain:
            if specific_domain not in user.email():
                self.abort(401)
        if not user:
            self.abort(401)

