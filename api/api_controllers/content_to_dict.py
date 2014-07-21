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

    return data