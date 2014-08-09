from flask.views import MethodView
from flask import render_template, abort
from google.appengine.api import users
from models.curriculum import Curriculum
from models.content import Content
from models.user import User, AppUser
from google.appengine.ext import ndb
from controllers.fetch_user import get_user_by_google_id
from controllers.new_course import new_course
from controllers.new_unit import new_unit
from controllers.new_lesson import new_lesson
import logging

class MigratePage(MethodView):
    def get(self, migration_type=None):
        current_user = users.get_current_user()
        if current_user.email() != 'quentin@lessonwell.com':
            abort(403)
        else:
            if migration_type == 'clear_content':
                ndb.delete_multi(Curriculum.query().fetch(keys_only=True))

            elif migration_type == 'clear_teacher_courses':
                teachers = User.query()
                for teacher in teachers:
                    logging.info('clearing courses for %s' % teacher.key.id())
                    teacher.courses = []
                    teacher.put()
                    logging.info('Completed clearing courses for %s' % teacher.key.id())

            elif migration_type == 'course':
                courses = Content.query(Content.contentType == 'course')
                for course in courses:
                    if course.listed != 'done_migrating3':
                        try:
                            logging.info("Begin course migration for %s" % course.key.id())
                            app_user = course.key.parent().get()
                            teacher = get_user_by_google_id(app_user.googleID)
                            course_data = {
                                'teacher' : teacher.key.id(),
                                'title' : course.title,
                                'body' : course.body
                            }
                            new_course_id = new_course(course_data)
                            logging.info("Saved data for Curriculum ID: %s" % new_course_id)
                            units = Content.query(Content.contentType == 'unit', ancestor=course.key)
                            for unit in units:
                                logging.info("Begin unit migration for %s" % unit.key.id())
                                unit_data = {
                                    'teacher' : teacher.key.id(),
                                    'course' : new_course_id,
                                    'title' : unit.title,
                                    'body' : unit.body
                                }
                                new_unit_id = new_unit(unit_data)
                                logging.info("Saved data for Unit ID: %s" % new_unit_id)

                                lessons = Content.query(Content.contentType == 'lesson', ancestor=unit.key)
                                for lesson in lessons:
                                    logging.info("Begin lesson migration for %s" % lesson.key.id())
                                    lesson_data = {
                                        'teacher' : teacher.key.id(),
                                        'course' : new_course_id,
                                        'unit' : new_unit_id,
                                        'title' : lesson.title,
                                        'body' : lesson.body
                                    }
                                    lesson_id = new_lesson(lesson_data)
                                    logging.info("Saved data for Lesson ID: %s" % lesson_id)

                            course.listed = 'done_migrating3'
                            course.put()
                            logging.info("Finished course migration for %s" % course.key.id())
                        except Exception as e:
                            logging.info("Error migrating course %s" % course.key.id())
                            logging.info(str(e))


            return render_template(
                'migrate.html',
                status_msg = 'migration complete'
                )
