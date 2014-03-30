import webapp2
import json

class APIHandler(webapp2.RequestHandler):
    """
    API Handler inherited by all api request handlers to make things easier
    """

    def write_json(self, data):
        """
        take the passed data, add JSON headers, 
        and encode the data as a json string
        """
        self.response.headers['Content-Type'] = 'application/json' 
        self.response.out.write(json.dumps(data))