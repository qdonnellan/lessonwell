from flask.ext.restful import Resource, reqparse
from controllers.fetch_curriculum import get_course_by_id
import hashlib

class UnlockAPI(Resource):
    """
    api handler for testing passphrase for course
    """

    def get(self, course_id = None):
        status = False
        if course_id:
            course = get_course_by_id(course_id)
            if course:
                parser = reqparse.RequestParser()
                parser.add_argument('attempted_passphrase', type=str)
                args = parser.parse_args()
                hashed_real = hashlib.sha256(course.content['passphrase']).hexdigest()
                hashed_attempt = hashlib.sha256(args['attempted_passphrase']).hexdigest()
                if hashed_real == hashed_attempt:
                    status = True
        return {'status' : status}

