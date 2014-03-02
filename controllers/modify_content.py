from models.content import Content
from fetch_content import get_content

def add_or_edit_content(title, body, parentKEY, contentType, content=None, should_delete = None, privacy = None, listed = None):
    '''
    add content or edit content

    return the content ID after add/edit operation
    '''
    if content is None:
        contentID = newContent(title, body, parentKEY, contentType, privacy, listed)
        return contentID
    else:
        editContent(content.key.id(), title, body, parentKEY, should_delete, privacy, listed)
        return content.key.id() 

def new_content(title, body, parentKEY, contentType, privacy=None, listed=None):
    '''
    create a new content object

    return the id of the content object
    '''
    contentObject = Content(
        parent = parentKEY, 
        body = body, 
        title = title, 
        contentType = contentType, 
        privacy = privacy,
        listed = listed)
    key = contentObject.put()
    return key.id()

def edit_content(contentID, parentKEY, title=None, body=None, should_delete = None, privacy = None, listed = None):
    '''
    edit existing content object or delete object if should_delete == 'Delete'

    return the id of the content object
    '''
    contentObject = get_content(parentKEY, contentID)
    if should_delete == 'Delete':
        if contentObject is not None: contentObject.key.delete()
        return None
    else:
        if privacy == 'true': contentObject.privacy = 'private'
        if title: contentObject.title = title
        if body: contentObject.body = body
        if listed: contentObject.listed = listed

        key = contentObject.put()
        return key.id()

def activateContent(contentObject, activateType):
    '''
    activate otherwide decativated content
    '''
    if contentObject.active != activateType or contentObject.active is None:
        contentObject.active = activateType
        contentObject.put()