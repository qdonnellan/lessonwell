from fetch_user import get_user
from models.curriculum import Curriculum
from controllers.fetch_curriculum import get_content_by_id

def modify_content(modified_content, content_id):
    """
    edit existing content, return the id of that content object
    """
    content_object = get_content_by_id(content_id)
    if 'title' in modified_content:
        content_object.content['title'] = modified_content['title']

    if 'body' in modified_content:
        content_object.content['body'] = modified_content['body']

    if 'passphrase' in modified_content:
        passphrase = modified_content['passphrase']
        if passphrase and passphrase != '':
            content_object.content['passphrase'] = passphrase

    content_object.put()
    return content_id
    
