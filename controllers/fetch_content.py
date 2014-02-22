from models.content import Content
from google.appengine.ext import ndb

def get_content(parentKEY, contentID):
    '''
    get a content model given a parentKEY and contentID
    '''
    if contentID is None:
        return None
    elif not str(contentID).isdigit():
        raise NameError("Invalid content identifier")
    else:
        theKey = ndb.Key(Content, int(contentID), parent=parentKEY)
        return theKey.get()

def get_all_content(parentKEY, contentType):
    '''
    return an ordered, iterable ContentQuery object 

    each item in the iterable has a parent of parentKEY and a type of contentType
    '''
    if contentType == 'course':
        contentObject = Content.query(Content.contentType == contentType, ancestor=parentKEY).order(Content.created)
    else:
        contentObject = Content.query(Content.contentType == contentType, ancestor=parentKEY).order(Content.title)
    return contentObject

def get_listed_courses(sort):   
    '''
    return a Content Query iterable of courses that are marked as "listed" by their authors

    iterable is sorted by popularity by default, else is 'recent' is passed, then it is sorted by creation data
    '''
    if 'recent' in sort:
        contents = Content.query(Content.contentType == 'course', Content.listed == 'listed').order(-Content.created)
    else:
        contents = Content.query(Content.contentType == 'course', Content.listed == 'listed').order(-Content.popularity)
    return contents

def get_all_courses():
    '''
    get all courses in the database
    '''
    contents = Content.query(Content.contentType == 'course')
    return contents
    