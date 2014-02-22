from handlers import MainHandler
from google.appengine.api import users
from new_database import *

class dbTransform(MainHandler):
	def get(self):
		if users.is_current_user_admin():
			allUsers = AppUser.query()
			for user in allUsers:
				user.username = user.username
				user.put()
				self.write('success')
		else:
			self.redirect('/')
