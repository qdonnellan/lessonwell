from handlers import MainHandler
from google.appengine.api import users
from new_database import getUser
from stripeHandlers import getCustomer, api_key
from stripeHandlers import donate as should_donate
import stripe
import re
import logging


class donate(MainHandler):
	def get(self, username):
		if should_donate:
			user = getUser(username)		
			if user is None:
				self.redirect('/?error=That user does not exist')
			else:
				customer = getCustomer(user)
				if customer.plan == 'free':
					self.redirect('/%s' % username)
				else:
					invoice = stripe.Invoice.upcoming(customer=user.stripeID, api_key = api_key)
					totalDonation = abs(int(invoice.starting_balance+invoice.total))			
					self.render('donation_page.html', totalDonation = totalDonation, user=user)
		else:
			self.redirect('/%s' % username)

	def post(self, username):
		if should_donate:
			token = self.request.get('stripeToken')
			user = getUser(username)
			amount = self.request.get('optionsRadios')
			amount = int(amount)
			try:
				newCharge = stripe.Charge.create(
					amount = amount,
					currency = 'usd',
					card = token,
					description = "donation",
					api_key = api_key
					)
			except Exception as e:
				self.redirect('/%s/donate?error=%s' % (username, e))
			else:
				stripe.InvoiceItem.create(
					customer = user.stripeID,
					amount = -amount,
					currency = 'usd', 
					description = 'donation received',
					api_key = api_key
					)
				self.render('donation_success.html', user =user)
		else:
			self.redirect('/%s' % username)


