import webapp2
import json

class APIHandler(webapp2.RequestHandler):
    '''
    API Handler inherited by all api request handlers to make things easier
    '''

    def write_json(self, data):
        self.response.headers['Content-Type'] = 'application/json' 
        self.response.out.write(json.dumps(data))