import webapp2
from views.public.front_page import FrontPage

app = webapp2.WSGIApplication([
  ('.*', FrontPage),
  ],debug=False)
