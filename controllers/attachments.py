from fetch_content import get_content

def edit_attachment(blob_info, parentKEY, contentID):
    '''
    edit the attachment belonging to this contentID with this parentKEY
    '''
    contentObject = get_content(parentKEY, contentID)
    blobs = contentObject.blobs
    if blobs is None:
        blobs = {}
    for new_blob in blob_info:
        if new_blob == 'lesson_attachment':
            blobs[blob_info['lesson_attachment']] = blob_info['lesson_attachment']
        else:
            blobs[new_blob] = blob_info[new_blob]
    contentObject.blobs = blobs
    contentObject.put()