from models.protectedNames import ProtectedNames 
from fetch_user import get_user_by_username
import re

def validate_username(username, localUser = None):
    '''
    verify that the given username is unique or raise a NameError exception
    '''
    if username in ProtectedNames:
        raise NameError("That username is protected, choose a different one")

    if re.match("^[a-zA-Z0-9]+$", username) is None:
        raise NameError("Your username may only contain numbers and letters")

    if len(username)<5 or len(username)>20:
        raise NameError("Your username must be at least 5 characters and no more than 20")

    if get_user_by_username(username) is not None:
        raise NameError("That username is already taken")