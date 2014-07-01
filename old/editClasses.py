from handlers import MainHandler, ProtectedHandler
from google.appengine.api import users
from new_database import edit_blobs, newContent, editContent, editUser, getContent, getAllContent, getUser, addOrEditContent, approved_users, get_standards
import auth
import markdown2
import logging
import re
from stripeHandlers import connectUrl, updateCustomer, verifyCourseLoad, verifyUnitLoad, verifyLessonLoad, api_key, verifyCustomer, addCoupon
import stripe
import datetime
import standards
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
import datetime


class editProfile(ProtectedHandler):
  def get(self):
    self.verify()
    localCustomer = auth.localCustomer()
    if self.localUser.user.stripeID != '':
      invoice = stripe.Invoice.upcoming(customer=self.localUser.user.stripeID, api_key = api_key) #useless when donation is disabled
      credit = int(invoice.starting_balance+invoice.total)  #useless when donation is disabled
      formatCredit = "%1.2f"  % abs(credit/100)  #useless when donation is disabled
      self.render('edit_profile.html',
        localCustomer = localCustomer,
        datetime = datetime,
        credit = credit,
        user = self.localUser,
        left_panel = True,
        formatCredit = formatCredit,  #useless when donation is disabled
        connect_url = connectUrl(self.localUser),
        coupon_error = self.request.get('coupon_error'))

  def post(self):
    self.verify()
    if 'redeem' in self.request.POST:
      code = self.request.get('coupon_code')
      coupon_event = addCoupon(code)
      if coupon_event == 'success':
        self.redirect('/edit_profile')
      else:
        self.redirect('/edit_profile?coupon_error=%s' % coupon_event)
    else:
      pic = self.request.get('pic')
      bio = self.request.get('bio')
      formalName = self.request.get('formalName
      success = editUser(
        pic = pic,
        bio = bio,
        formalName = formalName,
        localUser = self.localUser,)
      if success:
        self.redirect('/%s' % self.localUser.username)
      else:
        self.redirect('/edit_profile?error= something went wrong, try again')

class editCourse(blobstore_handlers.BlobstoreUploadHandler, ProtectedHandler):
  def get(self, courseID = None):
    self.verify()
    try:
      edit_url = '/new_course'
      course_image = None
      course = getContent(self.localUser.user.key, courseID)
      if course is not None:
        edit_url = '/edit_course/%s' % courseID
        if course.blobs is not None:
          if 'cover_image' in course.blobs:
            course_image = images.get_serving_url(course.blobs['cover_image'])
        access_amount = course.access_amount
        if access_amount in [0, None]:
          access_amount = None
        current_standards = standards.fetch(get_standards(self.localUser.user.key, courseID))
      else:
        access_amount = None
        current_standards = None
      status = verifyCourseLoad(self.localUser, course)
      self.render('edit_course.html',
        course = course,
        course_image = course_image,
        status = status,
        customer = verifyCustomer(self.localUser.user),
        approved_users = approved_users(course),
        amount_error = self.request.get('amount_error'),
        access_amount = access_amount,
        connect_url = connectUrl(self.localUser),
        current_standards = current_standards,
        upload_url = blobstore.create_upload_url(edit_url),
        ccss = standards.ccss,
        teks = standards.teks,
        left_panel = True,
        user = self.localUser,
        panel = self.request.get('panel'))
    except Exception as e:
      self.redirect('/%s?error=%s' % (self.localUser.username, e))

  def post(self, courseID = None):
    self.verify()
    course = getContent(self.localUser.user.key, courseID)
    if 'save_changes' in self.request.POST:
      title = self.request.get('courseName')
      body = self.request.get('description')
      course_privacy = self.request.get('course_privacy')
      course_listed = self.request.get('course_listed')
      courseID = addOrEditContent(
        title = title,
        body = body[:200],
        parentKEY = self.localUser.user.key,
        contentType = 'course',
        content = course,
        privacy = course_privacy,
        listed = course_listed)

      image_file = self.get_uploads()
      if image_file not in [None, '', []]:
        blob_info = image_file[0]
        edit_blobs({'cover_image' : str(blob_info.key())}, self.localUser.user.key, courseID)
      self.redirect('/%s/course%s' % (self.localUser.username, courseID))

    elif 'setup_money' in self.request.POST:
      if courseID is not None:
        amount = self.request.get('access_amount')
        if amount == '':
          course.access_amount = 0
          course.put()
          self.redirect('/edit_course/%s?panel=sell' % courseID)
        elif not amount.isdigit():
          self.redirect('/edit_course/%s?amount_error=Only enter an integer amount&panel=sell' % courseID)
        else:
          course.access_amount = int(amount)
          course.put()
          self.redirect('/edit_course/%s?panel=sell' % courseID)
    elif 'set_passphrase' in self.request.POST:
      if course is not None:
        passphrase = self.request.get('passphrase')
        course.passphrase = passphrase
        course.put()
        self.redirect('/edit_course/%s?panel=access' % courseID)


class editUnit(ProtectedHandler):
  def get(self, courseID, unitID = None):
    self.verify()
    try:
      course = getContent(self.localUser.user.key, courseID)
      unit = getContent(course.key, unitID)
      self.render('edit_unit.html',
        course = course,
        unit = unit,
        status = verifyUnitLoad(self.localUser, course, unit),
        user = self.localUser,
        left_panel = True)
    except Exception as e:
      self.redirect('/%s?error=%s' % (self.localUser.username, e))

  def post(self, courseID, unitID = None):
    self.verify()
    course = getContent(self.localUser.user.key, courseID)
    unit = getContent(course.key, unitID)
    title = self.request.get('unitName')
    body = self.request.get('description')
    should_delete = self.request.get('should_delete')
    unitID = addOrEditContent(title, body, course.key, 'unit', unit, should_delete=should_delete)
    self.redirect('/%s/course%s/unit%s' % (self.localUser.username, courseID, unitID))

class editLesson(blobstore_handlers.BlobstoreUploadHandler, ProtectedHandler):
  def get(self,courseID, unitID, lessonID = None):
    self.verify()
    try:
      course = getContent(self.localUser.user.key, courseID)
      unit = getContent(course.key, unitID)
      lesson = getContent(unit.key, lessonID)
      if lessonID is None:
        edit_url = '/add_lesson/%s/%s?panel=attach' % (courseID, unitID)
      else:
        edit_url = '/edit_lesson/course%s/%s/%s?panel=attach' % (courseID, unitID, lessonID)

      self.render('edit_lesson.html',
        course = course,
        unit = unit,
        lesson = lesson,
        user = self.localUser,
        status = verifyLessonLoad(self.localUser, unit, lesson),
        course_standards = get_standards(self.localUser.user.key, courseID),
        panel = self.request.get('panel'),
        upload_url = blobstore.create_upload_url(edit_url),
        left_panel = True,
        )
    except Exception as e:
      self.redirect('/%s?error=%s' % (self.localUser.username, e))

  def post(self, courseID, unitID, lessonID = None):
    self.verify()
    if 'save_lesson' in self.request.POST:
      course = getContent(self.localUser.user.key, courseID)
      unit = getContent(course.key, unitID)
      lesson = getContent(unit.key, lessonID)
      title = self.request.get('lessonName')
      body = self.request.get('content')
      should_delete = self.request.get('should_delete')
      lessonID = addOrEditContent(title, body, unit.key, 'lesson', lesson, should_delete = should_delete)
      self.redirect('/%s/course%s/unit%s?lesson=lesson%s' % (self.localUser.username, courseID, unitID, lessonID))
    elif 'upload' in self.request.POST:
      course = getContent(self.localUser.user.key, courseID)
      unit = getContent(course.key, unitID)
      lesson = getContent(unit.key, lessonID)
      blob_file = self.get_uploads()
      if blob_file not in [None, '', []]:
        blob_info = blob_file[0]
        edit_blobs({'lesson_attachment' : str(blob_info.key())}, unit.key, lessonID)

      self.redirect('/edit_lesson/course%s/%s/%s?panel=attach' % (courseID, unitID, lessonID))
