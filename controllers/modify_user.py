from models.user import User
from fetch_user import get_user_by_username
from validation import validate_username

def new_user(username, formalName, email, googleID, stripeID=None):
    """
    create a new user, return the user Object
    """
    validate_username(username)
    userObject = User(
        username = username,
        formalName = formalName,
        googleID = googleID,
        stripeID = stripeID,
        email = email,
        bio = '',
        parent = None,
        courses = [],
        )
    userObject.put()
    return userObject

def edit_user(username, formalName=None, bio=None, pic=None, stripeID=None):
    """
    edit an existing user by their username, return the user object
    """
    user = get_user_by_username(username)
    if user:
        if formalName: user.formalName = formalName
        if bio: user.bio = bio
        if pic: user.pic = pic
        if stripeID: user.stripeID = stripeID
        user.put()
        return user
    else:
        return False
