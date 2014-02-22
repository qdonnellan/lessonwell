from handlers import MainHandler
import logging
import hashlib
from format import shorthand
import standards
import new_database
import auth

class quizHandler(MainHandler):
  def post(self):
    quizID = self.request.get('quiz-identity')
    answer = self.request.get(quizID)    
    verification = self.request.get('quiz-verify')
    answer_hash = hashlib.sha1(answer).hexdigest()

    if hashlib.sha1(answer).hexdigest() == verification:
      my_response = 'true'
    else:
      my_response = 'false'

    self.response.out.write(my_response)

class formatHandler(MainHandler):
  def post(self):
    content = self.request.get('content')
    self.response.out.write(shorthand(content))

class standardsHandler(MainHandler):
  def post(self, courseID):
    localUser = auth.localUser() 
    course = new_database.getContent(localUser.user.key, courseID)
    should_delete = self.request.get('should_delete')
    if should_delete == 'true': 
      standard_id = self.request.get('standard_id')
      updated_standards = new_database.delete_standard(standard_id, localUser.user.key, courseID)     
      html = 'true' 
          
    else:
      form_standards = self.request.get_all('standards-checked')
      updated_standards = new_database.change_standards(form_standards, localUser.user.key, courseID) 
      html = self.render_str('standards_list.html', 
        current_standards = standards.fetch(updated_standards), 
        localUser = localUser,
        course = course)
            
    self.response.out.write(html)


