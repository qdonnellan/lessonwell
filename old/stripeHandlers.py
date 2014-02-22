from google.appengine.api import users
import stripe
import auth
import logging
from new_database import assignStripeID, getAllContent, activateContent, getAppCustomer, setAppCustomer
from google.appengine.api import memcache
import datetime
import urllib, urllib2

# stripe keys are imported from the stripe_keys file, this is private on purpose
# and included in the .gitignore file
from stripe_keys import *

stripe_publish_key = pub_key

def updateCustomer(plan, newcard, CVC, month, year, trial_end=None):
	localUser = auth.localUser()
	if localUser.exists:
		if localUser.user.stripeID is not None:
			cu = stripe.Customer.retrieve(localUser.user.stripeID, api_key = api_key)			
			if newcard not in ['', None]:
				cardDict = {
						'number' : newcard.replace(' ', ''),
						'exp_month' : month,
						'exp_year' : year, 
						'cvc' : CVC
						}
				cu.card = cardDict
				cu.save()

			if cu.subscription.plan.name != plan and plan not in ['', None]:
				limits = {
					'plus'	: [999,999,999],
					'basic' : [3,999,999],
					'free'  : [3,999,999]
				}
				if plan in limits:
					course_limit, unit_limit, lesson_limit = limits[plan]
					activateEverything('inactive', localUser.user)
					activateOnly(localUser.user, course_limit, unit_limit, lesson_limit)

				if trial_end is not None:
					cu.update_subscription(plan=plan, trial_end = trial_end)
				else:
					cu.update_subscription(plan=plan)
				getCustomer(localUser.user, refresh=True)

			if plan in ['', None]:
				activateEverything('inactive', localUser.user)

def addCoupon(coupon_code):
	localUser = auth.localUser()
	if localUser.exists:
		if localUser.user.stripeID is not None:
			try:
				cu = stripe.Customer.retrieve(localUser.user.stripeID, api_key = api_key)	
				cu.coupon = coupon_code
				cu.save()
				return 'success'
			except Exception as e:
				return e


def getCustomer(user, refresh=False):
	customer = getAppCustomer(user)
	if customer is None or refresh:
		if user.stripeID == '':
			customer = None
		else:
			customer = stripe.Customer.retrieve(user.stripeID, api_key = api_key)
			customer = setAppCustomer(user, customer)
	return customer

def verifyCustomer(user):
	customer = getCustomer(user)
	if customer is not None:
		timeDiff = customer.last_modified - datetime.datetime.utcnow()
		if 86400-timeDiff.seconds > 86400:
			customer = getCustomer(user, refresh = True)
			if customer.delinquent:
				activateEverything('inactive', localUser.user)
				activateOnly(localUser.user, 3, 999, 999)
	return customer

def activateEverything(activeType, user):
	allCourses = getAllContent(user.key, "course")
	for course in allCourses:
		activateContent(course, activeType)
		allUnits = getAllContent(course.key, "unit")
		for unit in allUnits:
			activateContent(unit, activeType)
			allLessons = getAllContent(unit.key, "lesson")
			for lesson in allLessons:
				activateContent(lesson, activeType)

def activateOnly(user, courseLimit, unitLimit, lessonLimit):
	allCourses = getAllContent(user.key, "course")
	courseCount = 0
	for course in allCourses:
		courseCount  += 1
		if courseCount <= courseLimit:
			activateContent(course, 'active')

		unitCount = 0	
		allUnits = getAllContent(course.key, "unit")
		for unit in allUnits:
			unitCount  += 1
			if unitCount <= unitLimit:
				activateContent(unit,  'active')

			lessonCount = 0			
			allLessons = getAllContent(unit.key, "lesson")
			for lesson in allLessons:
				lessonCount += 1
				if lessonCount <= lessonLimit:
					activateContent(lesson,  'active')

def verifyCourseLoad(localUser, course = None):
	if course is not None:
		#don't neet to check course load if course already exists!
		return True
	else:
		cu = stripe.Customer.retrieve(localUser.user.stripeID, api_key = api_key)
		count = getContentCount(localUser.courses)		
		planID = cu.subscription.plan.id
		allowable = {'free':3, 'basic':3, 'plus':999, 'max':999}
		if count < allowable[planID]:
			return True

def verifyUnitLoad(localUser, course, unit = None):
	return True #deprecated function

def verifyLessonLoad(localUser, unit, lesson = None):
	return True #deprecated function

def getContentCount(allContent):
	count = 0
	for content in allContent:
		count+=1
	return count

def connectUrl(localUser):
	params = {
		'response_type':'code',
		'stripe_user[url]':"http://www.lessonwell.com/%s" % localUser.username,
		'stripe_user[email]':localUser.user.email,
		'stripe_landing':'register',
		'client_id':connect_client_id,
		'stripe_user[business_type]':'sole_prop',
		'stripe_user[physical_product':'false',
		'scope':'read_write'

	}
	encoded = '?'
	for key in params:
		encoded += '%s=%s&' % (key, params[key])

	return "https://connect.stripe.com/oauth/authorize%s" % encoded


