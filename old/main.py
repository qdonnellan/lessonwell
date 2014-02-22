import webapp2
from google.appengine.api import users
from handlers import MainHandler, ProtectedHandler
from editClasses import editProfile, editCourse, editUnit, editLesson
from viewClasses import viewUnit, viewCourse, viewProfile
import new_database
from admin import *
import appErrors
from helpClasses import viewDocs, editDocs, help
import stripeHandlers
import stripe
import auth
import datetime
from donation import donate
from playground import playground
from ajax import quizHandler, formatHandler, standardsHandler
from blobs import ServeHandler, DeleteBlob
import urllib, urllib2
import json 
from format import shorthand

class terms(MainHandler):
    def get(self):
        self.redirect('/about?doc=terms')

class signUp(MainHandler):
    def get(self, planID):
        current_google_user = users.get_current_user()
        should_upgrade = self.request.get('upgrade')
        localUser = auth.localUser()
        if current_google_user is None:
            self.redirect('/link/%s' % planID)
        else:
            if planID not in ['free', 'plus']:
                planID = 'free'
            try:
                plan = stripe.Plan.retrieve(planID, api_key = stripeHandlers.api_key)
                trialEnd = datetime.datetime.now() + datetime.timedelta(days=plan.trial_period_days)
                expiredTrial = False
                localCustomer = auth.localCustomer()
                planAmount = plan.amount/100
                planAmount = "%1.2f"  % planAmount                       
                trialEnd = trialEnd.strftime("%A, %B %d").replace(' 0', ' ')
                self.render(
                    'sign_up.html', 
                    plan= plan, 
                    trialEnd = trialEnd, 
                    localCustomer = localCustomer, 
                    planAmount = planAmount, 
                    expiredTrial = expiredTrial,
                    googleEmail = current_google_user.email(),
                    should_upgrade = should_upgrade,
                    left_panel = True
                    )
            except Exception as errorMessage:
                self.redirect('/sign_up/%s?error= There was an error: %s' % (planID,errorMessage))

    def post(self, planID):
        username = self.request.get('username')
        should_upgrade = self.request.get('upgrade')
        try:
            token = self.request.get('stripeToken')          
            planOption = self.request.get('optionsPlan')
            current_google_user = users.get_current_user()
            termsChecked = 'sdfSJSkjnsd' #self.request.get('termsChecked')
            if termsChecked != 'sdfSJSkjnsd':
                raise NameError(appErrors.terms_not_accepted())
            if current_google_user is None:                
                raise NameError(appErrors.google_user_not_found())   
            elif 'updateUser' in self.request.POST:
                plan = self.request.get('optionsPlan')
                localCustomer = auth.localCustomer()
                card_on_file = localCustomer.customer.active_card
                newcard = self.request.get('c-number')
                if plan != 'free' and card_on_file is None and newcard in ['', None]:
                    raise NameError("You must have a credit card on file for a paid plan")
                stripeHandlers.updateCustomer(
                    plan = plan, 
                    newcard = newcard,
                    CVC = self.request.get('c-cvc'), 
                    month = self.request.get('c-exp-month'),
                    year = self.request.get('c-exp-year')
                    )
            else:
                user = new_database.newUser(
                    username = username, 
                    formalName = self.request.get('formalName'), 
                    email = current_google_user.email(), 
                    googleID = current_google_user.user_id(),
                    stripeID = "" 
                    )
                if user is not None:
                    if token in ['', None]:
                        customer = stripe.Customer.create(
                            plan=self.request.get('optionsPlan'),
                            email=current_google_user.email(),
                            description = str(current_google_user.user_id()),
                            api_key = stripeHandlers.api_key
                            )
                        user.stripeID = customer.id
                        user.put()
                    else:
                        customer = stripe.Customer.create(
                            card=token,
                            plan=self.request.get('optionsPlan'),
                            email=current_google_user.email(),
                            description = str(current_google_user.user_id()),
                            api_key = stripeHandlers.api_key
                            )
                        user.stripeID = customer.id
                        user.put()                     
        except Exception as errorMessage:  
            if should_upgrade == 'true':
                self.redirect('/sign_up/%s?upgrade=true&error= There was an error creating your account: %s' % (planID,errorMessage))
            else:
                self.redirect('/sign_up/%s?error= There was an error creating your account: %s' % (planID,errorMessage))            
        else:
            if should_upgrade == 'true':                
                self.redirect('/success?upgrade=true')
            else:               
                self.redirect('/success')

class changeCard(ProtectedHandler):
    def get(self):
        self.verify()
        self.render('change_card.html', localCustomer = auth.localCustomer(), left_panel = True)

    def post(self):
        self.verify()
        try:
            token = self.request.get('stripeToken')
            cu = stripe.Customer.retrieve(self.localUser.user.stripeID, api_key = stripeHandlers.api_key)
            cu.card = token
            cu.save()
        except Exception as e:
            self.redirect('/change_card?error=%s' % e)
        else:
            self.redirect('/%s' % self.localUser.username)


class success(MainHandler):
    def get(self): 
        should_upgrade = self.request.get('upgrade')
        self.render('success.html', upgrade = should_upgrade, left_panel = True)

class privacy(MainHandler):
    def get(self):
        self.redirect('/about?doc=privacy')

class monetize(MainHandler):
    def get(self):
        self.render('monetize.html')

class compsci(MainHandler):
    def get(self):
        sample_quiz = '''
quiz::
What is missing in the first line of the code below?

code::
def my_func(x)
  print x*2
::code

@@ A semi-colon at the end of the line
@@ A colon at the end of the line**
@@ Nothing, this code is perfectly fine!
::quiz
        '''
        self.render('cs_landing.html', sample_quiz = shorthand(sample_quiz))

class catalog(MainHandler):
    def get(self):
        sort = self.request.get('sort')
        listed_courses = new_database.get_listed_courses(sort)
        self.render('catalog.html', listed_courses = listed_courses, coursesActive = 'active', sort = sort)

class initpop(MainHandler):
    def get(self):
        contents = new_database.get_all_courses()
        for content in contents:        
            content.popularity = 0
            content.put()
        self.write('done')

class pricing(MainHandler):
    def get(self):
        self.render('pricing_new.html', localCustomer = auth.localCustomer())

class promotion(MainHandler):
    def get(self):
        self.render('promotion.html')

class about(MainHandler):
    def get(self):
        self.render('about.html', doc = self.request.get('doc'), left_panel = True)

class approvalHandler(ProtectedHandler):
  def get(self, courseID, googleID, status):
    self.verify()
    course = new_database.getContent(self.localUser.user.key, courseID)
    if course is not None:
      new_database.update_approval(course, googleID, status)
    self.redirect('/edit_course/%s?panel=access' % courseID)

class linkAccount(MainHandler):
    def get(self, planID):
        googleUser = users.get_current_user()
        logoffURL = users.create_logout_url('/link/%s' % planID)
        self.render('link.html', 
            googleUser = googleUser, 
            logoffURL = logoffURL, 
            planID = planID,
            loginURL = users.create_login_url('/sign_up/%s' % planID),
            left_panel = True
            )

class stripeConnect(MainHandler):
    def get(self):
        code = self.request.get('code')
        state = self.request.get('state')
        if code is None:
            self.redirect('/')
        else:
            params = {
                'client_secret' : stripeHandlers.api_key,
                'code' : code,
                'grant_type' : 'authorization_code'}
            url = "https://connect.stripe.com/oauth/token"
            try:
                request = urllib2.Request(url, urllib.urlencode(params))
                response =urllib2.urlopen(request)
                response = json.load(response)
                if 'error' not in response:
                    localUser = auth.localUser()            
                    localUser.user.populate(
                        stripe_pub_key =  response["stripe_publishable_key"],
                        stripe_access_token = response["access_token"]
                        )
                    localUser.user.put()
                if 'course' in state:
                    courseID = re.search('course(\d+)', state)
                    if courseID is not None:
                        self.redirect('/edit_course/%s#sell-access' % courseID.group(1))
                    else:
                        self.redirect('/edit_profile')
                self.redirect('/edit_profile') 
            except Exception as e:
                self.redirect('/edit_profile?connect_error=%s' % e)       

app = webapp2.WSGIApplication([
    ('/link/(\w+)', linkAccount),
    ('/edit_profile', editProfile),
    ('/edit_course/(\w+)', editCourse),
    ('/add_unit/(\w+)', editUnit),
    ('/add_lesson/(\w+)/(\w+)', editLesson),
    ('/edit_unit/course(\w+)/(\w+)', editUnit),
    ('/edit_lesson/course(\w+)/(\w+)/(\w+)', editLesson),
    ('/new_course', editCourse),
    ('/(\w+)/course(\w+)/unit(\w+)', viewUnit),
    ('/(\w+)/course(\w+)', viewCourse),
    ('/edit_docs/(\w+)/(\w+)', editDocs),
    ('/edit_docs/(\w+)', editDocs),
    ('/help/(\w+)', viewDocs),
    ('/tos', terms),
    ('/help', help),
    ('/pricing', pricing),
    ('/monetize', monetize),
    ('/cs', compsci),
    ('/about', about),
    ('/catalog', catalog),
    ('/sign_up/(\w+)', signUp),
    ('/privacy', privacy),
    ('/success', success),
    ('/ajax_quiz', quizHandler),
    ('/ajax_format', formatHandler),
    ('/ajax_standards/(\w+)', standardsHandler),
    ('/change_card', changeCard),
    ('/stripe_connect', stripeConnect),
    ('/db_transform', dbTransform),
    ('/playground', playground),
    ('/attachment/([^/]+)?', ServeHandler),
    ('/promotion', promotion),
    ('/delete_attachment/([^/]+)?/([^/]+)?/([^/]+)?/([^/]+)?', DeleteBlob),
    #('/initpop', initpop),
    ('/approval/(\w+)/(\w+)/(\w+)', approvalHandler), 
    ('/(\w+)', viewProfile),
    ('.*', MainPage)
    ],debug = True)