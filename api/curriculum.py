from flask.ext.restful import Resource, reqparse

from controllers.fetch_curriculum import get_content_by_id
from api.api_controllers.content_to_dict import content_to_dict
from decorators.auth import check_approval, local_user_required
from google.appengine.api import users
from controllers.fetch_user import get_user_by_google_id
from controllers.new_course import new_course
from controllers.new_unit import new_unit
from controllers.new_lesson import new_lesson
from controllers.modify_curriculum import modify_content, delete_content
import logging
import re

class CurriculumAPI(Resource):
    """
    handle all get/post requests for curriculum type things
    """

    def get(self, content_id):
        """
        handle the get request for the CurriculumAPI,
        exceptions are caught and passed in the 'error' param
        """
        try:
            content = get_content_by_id(content_id)
            data = content_to_dict(content)
            logging.info('made it here 1')
            if content.content_type == 'course':
                logging.info('made it here 2')
                unit_list = []
                for unit_id in content.content['units']:
                    logging.info('made it here in unit: %s' % unit_id)
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
            return {'error' : str(e)}, 500
        else:
            return data

    def post(self, content_id=None):
        """
        handle the post request for the CurriculumAPI

        if no content_id then assumption is new entity, else the assumption
        is to edit an existing entity
        """
        if not users.get_current_user():
            return {'error': 'you must be logged in'}, 401
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('content_type', type=str)
            parser.add_argument('teacher', type=str)
            parser.add_argument('title', type=str)
            parser.add_argument('body', type=str)
            parser.add_argument('private', type=str)
            parser.add_argument('course', type=str)
            parser.add_argument('unit', type=str)
            args = parser.parse_args()
            try:
                content = {}
                content_type = args['content_type']

                if content_type not in ['course', 'unit', 'lesson']:
                    raise TypeError('invalid content type')

                googleID = users.get_current_user().user_id()
                content['teacher'] = get_user_by_google_id(googleID).key.id()
                if content_type == 'lesson':
                    # the first line of the lesson body IS the title
                    title = args['body'].strip().splitlines()[0]
                    content['title'] = re.sub('^#+', '', title)
                else:
                    content['title'] = args['title']
                content['body'] = args['body']
                content['private'] = args['private']
                if not content_id:
                    if content_type == 'course':
                        content_id = new_course(content)
                    if content_type == 'unit':
                        content['course'] = args['course']
                        content_id = new_unit(content)
                    if content_type == 'lesson':
                        content['unit'] = args['unit']
                        content_id = new_lesson(content)

                else:
                    modify_content(content, content_id)

                new_content = get_content_by_id(content_id)
                data = content_to_dict(new_content)
            except Exception as e:
                logging.info(e)
                return {'error' : str(e)}, 500
            else:
                return data

    def delete(self, content_id):
        """
        delete the associated content
        """
        if not users.get_current_user():
            return {'error': 'you must be logged in'}, 401
        else:
            try:
                delete_content(content_id)
            except Exception as e:
                logging.info(e)
                return {'error' : str(e)}, 500
            else:
                return 200


