def check_privacy(course):
    '''
    return true if course is private and false otherwise
    '''
    if not course:
        raise Exception('cannot check the privacy of NoneType course')
    else:
        if course.privacy == 'private':
            return True 
        else:
            return False