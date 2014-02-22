from handlers import MainHandler
from format import shorthand
import logging
import urllib   
import re

class playground(MainHandler):
  def get(self):
    example = self.request.query_string
    # example is the entire query string, potentially holding an example content
    # which will be injected into the form for the user to see
    # See examples.py for the current standard examples
    if 'example=' in example:
      example = re.sub('example=', '', example)
      example = urllib.unquote(example)
    else:
      example = ''
    self.render('playground.html', example = example, formatted_example = shorthand(example))

  def post(self):
    the_content = self.request.get('content')
    self.render('playground.html', 
      the_content_formatted = shorthand(the_content),
      the_content_unformatted = the_content
      )
