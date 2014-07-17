from controllers.fetch_user import get_active_user
import logging

def content_to_dict(content):
    """
    return a dictionary object based on the curriculum model passed
    """

    data = {}
    data['content_type'] = content.content_type
    data['id'] = content.key.id()
    data['content'] = content.content

    data['is_private'] = False

    if data['content']['passphrase']:
        data['is_private'] = True
        passphrase = ''
        user = get_active_user()
        if 'teacher' in data['content']:
            if user and user.key.id() == data['content']['teacher']:
                # if it's the teacher, OK to show passphrase
                passphrase = data['content']['passphrase']
                data['is_private'] = False
                 
        data['content']['passphrase'] = passphrase

    logging.info(data)

    return data