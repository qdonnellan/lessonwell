def content_to_dict(content):
    '''
    return a dictionary object based on the content model passed
    '''

    data = {}

    data['content_type'] = content.contentType 
    data['title'] = content.title
    data['parent_id'] = content.key.parent().id()
    data['id'] = content.key.id()
    data['body'] = content.body
    data['active'] = content.active
    data['last_modified'] = content.last_modified.strftime("%Y-%m-%d %H:%M:%S")
    data['created'] = content.created.strftime("%Y-%m-%d %H:%M:%S")
    data['listed'] = content.listed
    data['privacy'] = content.privacy
    data['access_amount'] = content.access_amount
    data['passphrase'] = content.passphrase

    return data