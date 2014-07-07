from flask.ext.restful import Resource, reqparse
from models.user import User
from google.appengine.ext import ndb
from controllers.modify_user import edit_user
from controllers.fetch_user import get_user_by_google_id
from api.api_controllers.user_to_dict import user_to_dict
from google.appengine.api import users

class UsersAPI(Resource):
    """
    api handlers for user objects
    """
    def get(self, user_id = None):
        """
        return the user if user_id provided, else return the users queryset
        """
        if user_id:
            user = ndb.Key(User, int(user_id)).get()
            if not user:
                return {'message':'user does not exist'}, 400
            else:
                google_user = users.get_current_user()
                data = user_to_dict(user)
                return data

        else:
            all_users = User.query()
            user_list = []
            for user in all_users:
                user_dict = user.to_dict()
                user_dict['id'] = user.key.id()
                user_list.append(user_dict)
            return {'users' : user_list}

    def post(self, user_id = None):
        """
        a post request is a NEW user
        """
        return {'message' : 'not implemented yet!'}

    def put(self, user_id):
        """
        a put request updates an existing user
        """
        parser = reqparse.RequestParser()
        parser.add_argument('formalName', type=str)
        parser.add_argument('stripeID', type=str)
        parser.add_argument('bio', type=str)
        #parser.add_argument('plan', type=str)
        args = parser.parse_args()
        user = ndb.Key(User, int(user_id)).get()
        if not user:
            return {'message':'user does not exist'}, 400
        else:
            if args['formalName']: user.formalName = args['formalName']
            if args['bio']: user.bio = args['bio']
            if args['stripeID']: user.stripeID = args['stripeID']
            user.put()
            return user_to_dict(user)

    

        

