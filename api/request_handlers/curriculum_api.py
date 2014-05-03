from main_api_handler import APIHandler
from controllers.fetch_curriculum import get_content_by_id
from api.api_controllers.content_to_dict import content_to_dict
from decorators.auth import check_approval, local_user_required
from google.appengine.api import users
from controllers.fetch_user import get_user_by_google_id
from controllers.new_course import new_course
from controllers.new_unit import new_unit
from controllers.new_lesson import new_lesson
from controllers.modify_curriculum import modify_content
import logging
import re

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
            if content.content_type == 'unit':
                lesson_list = []
                for lesson_id in content.content['lessons']:
                    lesson = get_content_by_id(lesson_id)
                    lesson_list.append(content_to_dict(lesson))
                data['lessons'] = lesson_list
        except Exception as e:
            data = {'error' : str(e)}

        self.write_json(data)

    @local_user_required
    def post(self, contentID=None):
        """
        handle the post request for the CurriculumAPI

        if no contentID then assumption is new entity, else the assumption
        is to edit an existing entity

        acceptable params of the data sent in the post request include:

        'content_type' : str
        'title' : str
        'body' : str
        'private' : bool
        """
        try:
            content_type = self.request.POST.get('content_type')
            if content_type not in ['course', 'unit', 'lesson']:
                raise TypeError('invalid content type')
            googleID = users.get_current_user().user_id()

            content = {}

            content['teacher'] = get_user_by_google_id(googleID).key.id()
            if content_type == 'lesson':
                # the first line of the lesson body IS the title
                body = self.request.POST.get('body')
                title = body.splitlines()[0]
                content['title'] = re.sub('^#+', '', title)
            else:
                content['title'] = self.request.POST.get('title')
            content['body'] = self.request.POST.get('body')
            content['private'] = self.request.POST.get('private')
            if contentID is None:
                if content_type == 'course':
                    contentID = new_course(content)
                if content_type == 'unit':
                    content['course'] = self.request.POST.get('course')
                    contentID = new_unit(content)
                if content_type == 'lesson':
                    content['unit'] = self.request.POST.get('unit')
                    contentID = new_lesson(content)

            else:
                modify_content(content, contentID)

            new_content = get_content_by_id(contentID)
            data = content_to_dict(new_content)
        except Exception as e:
            data = {'error' : str(e)}
        logging.info(data)
        self.write_json(data)
