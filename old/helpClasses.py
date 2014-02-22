from handlers import MainHandler
from new_database import getDocs, newDoc, getDocByID, editDocByID
from format import formatContent
from google.appengine.api import users

class viewDocs(MainHandler):
	def get(self, doctype):
		admin = users.is_current_user_admin()
		if doctype in ['shorthand', 'about', 'selling', 'getstarted']:
			allDocs = getDocs(doctype)
			formttedDocs = formatContent(allDocs, helpdoc=True)
			self.render('help_docs.html', allDocs = formttedDocs, doctype = doctype, admin = admin, helpActive = 'active', left_panel = True)
		else:
			self.redirect('/')

class editDocs(MainHandler):
	def get(self, doctype, docID=None):
		if users.is_current_user_admin():
			doc = getDocByID(docID)
			if doc is not None:
				self.render('edit_docs.html', doctype = doctype, docTitle = doc.title, docContent = doc.body)
			else:
				self.render('edit_docs.html', doctype = doctype)
		else:
			self.redirect('/')

	def post(self,doctype, docID=None):
		if users.is_current_user_admin():			
			title = self.request.get('docName')
			content = self.request.get('content')
			if docID is None:			
				docKeyID = newDoc(title = title, content = content, category = doctype)				
			else:
				editDocByID(title = title, content = content, docID = docID)
			self.redirect('/help/%s' % doctype)
		else:
			self.redirect('/')

class help(MainHandler):
	def get(self):
		self.render('help.html', helpActive = 'active', left_panel = True)