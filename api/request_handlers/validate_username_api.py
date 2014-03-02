from main_api_handler import APIHandler
from controllers.validation import validate_username

class ValidateUsernameAPI(APIHandler):
    '''
    handle the requests for a valid_username
    '''

    def get(self, username):
        ''' 
        return a json string with an 'error' param if username is bad or a 'success' param if valid
        '''
        try:
            validate_username(username)
        except Exception as e:
            data = {'error' : str(e)}
        else:
            data = {'error' : False}

        self.write_json(data)