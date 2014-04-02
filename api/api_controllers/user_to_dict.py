from controllers.fetch_curriculum import get_course_by_id
from content_to_dict import content_to_dict

def user_to_dict(user):
    """
    return a dictionary object based on the user model passed
    """
    data = {}

    data['username'] = user.username
    data['username_lower'] = user.username_lower
    data['id'] = user.key.id()
    data['googleID'] = user.googleID
    data['formal_name'] = user.formalName
    data['email'] = user.email
    data['bio'] = user.bio
    data['stripeID'] = user.stripeID
    data['courses'] = []
    if user.courses:
        for course_id in user.courses:
            course = get_course_by_id(course_id)
            data['courses'].append(content_to_dict(course))

    return data