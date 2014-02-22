from google.appengine.api import users
import new_database
import logging

class checkApproval():
  def __init__(self, course, author):
    self.status = False
    current_google_user = users.get_current_user()
    if current_google_user:
      approval = new_database.googleID_approval(course, current_google_user.user_id())
      if approval is not None:
        self.status = approval.status

      if str(author.googleID) == str(current_google_user.user_id()):
        self.status = 'approved'

