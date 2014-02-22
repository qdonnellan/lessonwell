from handlers import MainHandler
from new_database import getUser, getContent, getAllContent, approval_request, increase_popularity
from google.appengine.api import users
from format import formatContent
import format
from stripeHandlers import getCustomer, verifyCustomer
import stripe
import auth
import appErrors
import privacy
import logging
from google.appengine.api import memcache
from operator import attrgetter
import re


class viewUnit(MainHandler):
    def get(self, username, courseID, unitID):
        user = getUser(username)
        customer = verifyCustomer(user)
        try:
            if user is None:
                raise NameError(appErrors.DNE('user'))
            course = getContent(user.key, courseID)
            if course is None:
                raise NameError(appErrors.DNE('course'))
            unit = getContent(course.key, unitID)
            if unit is None:
                raise NameError(appErrors.DNE('unit'))
            allLessons = getAllContent(unit.key, "lesson")
            activeLessons, inactiveContent = detectActiveContent(allLessons)
            activeLessons = sort_by_param(activeLessons, 'title')
            access = privacy.checkApproval(course, user)
            active_lesson = self.request.get("lesson")
            if access.status not in ['approved', True, 'paid'] and course.privacy not in ['public', '', None]:
                self.redirect('/%s/course%s' % (username, courseID))
            else:
                ip = self.request.remote_addr
                if ip is not None:
                    recent_hit = memcache.get('%s_%s' % (courseID, ip))
                    if not recent_hit:
                        increase_popularity(course)
                        memcache.set('%s_%s' % (courseID, ip), 'recent_hit', 24*60*60)
                self.render('unit.html', 
                    course = course, 
                    user = user, 
                    customer = customer,
                    unit = unit, 
                    unitID = unitID, 
                    lessons = activeLessons, 
                    inactiveContent = inactiveContent,
                    emptyContent = detectEmptyContent(allLessons),
                    left_panel = True,
                    active_lesson = active_lesson
                    )
        except Exception as errorMessage:
            self.redirect('/?error= %s' % errorMessage)

class viewCourse(MainHandler):
    def get(self, username, courseID):
        user = getUser(username)
        logging.info(user)
        customer = verifyCustomer(user)
        try:
            if user is None:
                raise NameError(appErrors.DNE('user'))            
            course = getContent(user.key, courseID)            
            if course is None:
                raise NameError(appErrors.DNE('course'))
            if course.active == 'inactive':
                raise NameError(appErrors.inactive('course'))

            allUnits = getAllContent(course.key, "unit")
            activeUnits, inactiveContent = detectActiveContent(allUnits)  
            activeUnits = sort_by_param(activeUnits, 'title')           
            self.render('course.html', 
                course = course,
                user = user, 
                units = activeUnits,
                inactiveContent = inactiveContent,  
                emptyContent = detectEmptyContent(allUnits),
                access = privacy.checkApproval(course, user),
                current_google_user = users.get_current_user(),
                customer = customer,
                passphrase_error = self.request.get('passphrase_error'),
                loginURL = users.create_login_url('/%s/course%s' % (username, courseID)),
                left_panel = True
                )
        except Exception as errorMessage:
            self.redirect('/?error= %s' % errorMessage)

    def post(self, username, courseID):
        user = getUser(username)
        course = getContent(user.key, courseID)
        formalName = self.request.get('formalName')
        token = self.request.get('stripeToken')
        current_google_user = users.get_current_user()
        if token not in [None, '']:
            stripe.Charge.create(
                amount = course.access_amount*100,
                currency = "usd",
                card = token,
                description = "The user: %s purchased your course: %s" % (current_google_user.email(), course.title),
                api_key = user.stripe_access_token,
                application_fee = int(course.access_amount*100*(7.0/100))
                )                
            approval_request(
                course=course, 
                googleID=current_google_user.user_id(), 
                formalName=current_google_user.email(), 
                status='paid',
                email = current_google_user.email()
                )
            self.redirect('/%s/course%s' % (username, courseID))        
        else:
            passphrase = self.request.get('passphrase')
            if course.passphrase not in ['', None] and course.passphrase != passphrase:
                self.redirect('/%s/course%s?passphrase_error=true' % (username, courseID))
            else:
                approval_request(
                    course=course, 
                    googleID=current_google_user.user_id(), 
                    formalName=formalName, 
                    status='pending',
                    email = current_google_user.email()
                    )
                self.redirect('/%s/course%s' % (username, courseID))


class viewProfile(MainHandler):
    def get(self,username):
        user = getUser(username)    
        if user is None:
            self.redirect('/')  
        else:    
            try:
                
                allCourses = getAllContent(user.key, "course")
                activeCourses, inactiveContent = detectActiveContent(allCourses)
                if user.bio in ['', None]:
                    bio = user.bio
                else:
                    bio = format.shorthand(user.bio)          
                self.render('profile.html', 
                    user = user, 
                    bio = bio,
                    customer = verifyCustomer(user) ,
                    emptyContent = detectEmptyContent(allCourses),
                    courses = activeCourses,
                    inactiveContent = inactiveContent, 
                    profileActive = 'active', 
                    left_panel = True)
            except Exception as errorMessage:
                self.redirect('/?error=%s' % errorMessage)

class detectEmptyContent():
    def __init__(self, contentObject):
        count = 0
        for content in contentObject:
            count +=1
        if count == 0:
            self.exists = True
        else:
            self.exists = False

def detectActiveContent(allContent):
    activeContent = []
    inactiveCount = 0
    for content in allContent:
        if content.active != 'inactive':
            activeContent.append(content)
        else:
            inactiveCount += 1
    return activeContent, inactiveContent(inactiveCount)

class inactiveContent():
    def __init__(self,inactiveCount):
        self.count = inactiveCount
        if inactiveCount > 0:            
            self.exists = True
        else:
            self.exists = False

def natural_sort_key(key): 
    convert = lambda text: int(text) if text.isdigit() else text 
    return lambda s: [convert(c) for c in re.split('([0-9]+)', key(s))]

def sort_by_param(query_object, sort_param):
  alist = []
  for indiv_object in query_object:
    alist.append(indiv_object)
  if alist != []:
    return sorted(alist, key=natural_sort_key(attrgetter(sort_param)))
  else:
    return alist



