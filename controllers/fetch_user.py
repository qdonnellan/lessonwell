from models.user import User
from google.appengine.ext import ndb
from google.appengine.api import users

def get_user_by_username(username):
    """
    return the user object given their username
    """
    user = User.query(User.username_lower == username.lower()).get()
    return user

def get_user_by_google_id(googleID):
    """
    return the user object given their googleID
    """
    user = User.query(User.googleID == str(googleID)).get()
    return user

def get_user(userID):
    """
    return the user object given their userID
    """
    user = ndb.Key(User, int(userID)).get()
    return user

def get_active_user():
    """
    return the active user or None if there is None
    """
    active_user = None
    current_google_user = users.get_current_user()
    if current_google_user:
        active_user = get_user_by_google_id(current_google_user.user_id())
    return active_user


