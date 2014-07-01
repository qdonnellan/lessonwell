from google.appengine.api import users
from new_database import getUserByGoogleID, getAllContent, detectRequests
import stripe
import logging
import datetime
import privacy
from stripeHandlers import api_key

class localUser():
	# used for controlling the page style given a user state
	def __init__(self):
		self.exists = False
		self.username = None
		self.formalName = None
		self.email = ''
		self.bio = ''
		self.logoffURL = ''
		self.courses= []
		current_google_user = users.get_current_user()
		self.logonURL = users.create_login_url('/')
		if current_google_user is not None:
			user = getUserByGoogleID(current_google_user.user_id())
			if user is not None:
				self.username = user.username
				self.bio = user.bio
				self.pic = user.pic
				self.email = user.email
				self.formalName = user.formalName
				self.exists = True
				self.user = user
				self.logoffURL = users.create_logout_url('/')
				self.courses = getAllContent(user.key, "course")
				self.pending = detectRequests(user)

class localCustomer():
	def __init__(self):
		self.localUser = localUser()
		trialEnd = datetime.datetime.now()
		self.trialEnd = trialEnd.strftime("%A, %B %d").replace(' 0', ' ')
		self.expiredTrial = True
		self.planAmount = None
		self.exists = False
		if self.localUser.exists:
			if self.localUser.user is not None:
				if self.localUser.user.stripeID not in ['', None]:
					customer = stripe.Customer.retrieve(self.localUser.user.stripeID, api_key = api_key)
					if customer is not None:
						self.customer = customer
						if self.customer.subscription.trial_end is not None:
							trialEnd = datetime.datetime.fromtimestamp(self.customer.subscription.trial_end)
						if datetime.datetime.now() > trialEnd:
							self.expiredTrial = True
						else:
							self.expiredTrial = False
						self.trialEnd = trialEnd.strftime("%A, %B %d").replace(' 0', ' ')
						planAmount = self.customer.subscription.plan.amount/100
						if planAmount is not None:
							self.planAmount = "%1.2f"  % planAmount
						self.exists = True
