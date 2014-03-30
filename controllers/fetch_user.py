from models.user import User
from google.appengine.ext import ndb

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
