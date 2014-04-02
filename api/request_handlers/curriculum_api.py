from main_api_handler import APIHandler
from controllers.fetch_curriculum import get_content_by_id
from api.api_controllers.content_to_dict import content_to_dict
from decorators.auth import check_approval, local_user_required
from google.appengine.api import users
from controllers.fetch_user import get_user_by_google_id
from controllers.new_course import new_course
from controllers.new_unit import new_unit
import logging

class CurriculumAPI(APIHandler):
    """
    handle all get/post requests for content type things
    """

    @check_approval
    def get(self, contentID):
        """
        handle the get request for the CurriculumAPI, 
        exceptions are caught and passed in the 'error' param
        """
        try:
            content = get_content_by_id(contentID)
            data = content_to_dict(content)
            if content.content_type == 'course':
                unit_list = []
                for unit_id in content.content['units']:
                    unit = get_content_by_id(unit_id)
                    unit_list.append(content_to_dict(unit))
                data['units'] = unit_list
        except Exception as e:
            data = {'error' : str(e)}

        self.write_json(data)

