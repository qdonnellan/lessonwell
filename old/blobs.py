from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from handlers import ProtectedHandler
from new_database import getContent
import urllib

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    self.send_blob(blob_info, save_as=True)

class DeleteBlob(ProtectedHandler):
	def get(self, resource, courseID, unitID, lessonID):		
		self.verify()
		try:
			course = getContent(self.localUser.user.key, courseID)
			unit = getContent(course.key, unitID)
			lesson = getContent(unit.key, lessonID)
			resource = str(urllib.unquote(resource))
			blob_info = blobstore.BlobInfo.get(resource)
			lesson.blobs.pop(str(blob_info.key()), None)
			lesson.put()
			
			blob_info.delete()
			
			self.redirect('/edit_lesson/course%s/%s/%s?panel=attach' % (courseID, unitID, lessonID))
		except Exception as e:
			self.redirect('/?error=%s' % e)

