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

    return data