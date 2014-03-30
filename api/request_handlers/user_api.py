from main_api_handler import APIHandler
from controllers.fetch_user import get_user
from api.api_controllers.user_to_dict import user_to_dict

class UserAPI(APIHandler):
    """
    handle all get/post requests for the user api
    """

    def get(self, userID):
        """
        handle the get request userID; return none if userID does not exist
        """
        try:
            user = get_user(userID)
            if not user:
                raise Exception('that user does not exist')
            data = user_to_dict(user)

        except Exception as e:
            data = {'error' : str(e)}

        self.write_json(data)