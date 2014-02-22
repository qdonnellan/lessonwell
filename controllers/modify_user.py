from models.user import User
from fetch_user import get_user
from validation import validate_username

def new_user(username, formalName, email, googleID, stripeID=None):  
    '''
    create a new user, return the user Object
    '''
    validate_username(username)
    userObject = User(
        username = username, 
        formalName = formalName,
        tagline = '',
        googleID = googleID, 
        stripeID = stripeID,
        email = email,
        contentType = "user",
        parent = None,
        )
    userObject.put()
    return userObject

def edit_user(formalName, bio, pic, tagline, localUser):
    '''
    edit an existing user by their username, return the user object
    '''
    user = get_user(localUser.username)
    user.populate(
        formalName = formalName,
        bio = bio,
        pic = pic,
        tagline = tagline,      
        )
    user.put()
    return user

def assign_stripe_id(user, stripeID):
    '''
    assign a passed stripeID to the user
    '''
    user.stripeID = stripeID
    user.put()
