from main_api_handler import APIHandler
from controllers.fetch_content_by_id import get_content
from api.api_controllers.content_to_dict import content_to_dict
from decorators.auth import check_approval

class ContentAPI(APIHandler):
    '''
    handle all get/post requests for content type things
    '''

    @check_approval
    def get(self, userID=None, courseID=None, unitID=None, lessonID=None):
        ''' 
        handle the get request for the content api, exceptions are caught and passed in the 'error' param
        '''
        try:
            content = get_content(userID, courseID, unitID, lessonID)
            data = content_to_dict(content)
        except Exception as e:
            data = {'error' : str(e)}

        self.write_json(data)