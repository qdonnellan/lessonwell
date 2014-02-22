import os
import jinja2

class JinjaEnvironment:
    '''
    the templating environment
    '''

    def __init__(self):
        '''
        initialize the environment: set template folder location and load custom filters
        '''
        self.template_dir = os.path.join(os.path.dirname(__file__),"templates")
        self.environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            autoescape=True
        )
