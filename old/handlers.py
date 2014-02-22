import os
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.ext.blobstore import BlobInfo
from format import shorthand

import auth
from stripeHandlers import stripe_publish_key, connect_client_id, monetize, donate


template_dir=os.path.join(os.path.dirname(__file__),"templates")
jinja_environment=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_environment.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):  
    	alert = makeAlerts(error = self.request.get('error'), success = self.request.get('success'))                 
        self.write(self.render_str(template, 
            localUser = auth.localUser(), 
            alert = alert, 
            stripe_publish_key = stripe_publish_key, 
            monetize = monetize,
            donate = donate,
            images = images,
            BlobInfo = BlobInfo,
            shorthand = shorthand,
            **kw))
        
class ProtectedHandler(MainHandler):
    def verify(self):
        localUser = auth.localUser()
        if localUser.exists:
            self.localUser = localUser
        else:
            self.redirect('/?error=You do not have permission to do that')



class makeAlerts():
    def __init__(self, error = None, success = None):
        self.errorMsg = error
        self.successMsg = success
        if error is not None and error != '':
            self.errorDisplay = 'visible'
        else:
            self.errorDisplay = 'none'

        if success is not None and success != '':
            self.successDisplay = 'visible'
        else:
            self.successDisplay = 'none'





        
            
