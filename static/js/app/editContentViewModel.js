define(['./baseViewModel', 'knockout'], function (baseViewModel, ko) {

    return function editContentViewModel() {
        var self = this;
        // editContentViewModel inherits from the baseViewModel
        ko.utils.extend( self, new baseViewModel() );

        
        self.customer_loaded = ko.observable(false);

        self.sponsored = ko.computed(function() {
            var status = false;
            if ( self.customer_loaded() ) {
                var sub = self.subscription();
                if ( sub && sub.discount ) {
                    if ( sub.discount.coupon.id == 'sponsored' ) {
                        status = true;
                    }
                }
            }
            return status;
        });

        self.plan = ko.observable('');
        self.last_four = ko.computed(function() {
            if (self.last_four_raw() === null ) {
                return 'loading...';
            } else if (self.last_four_raw() === false) {
                return 'No card on file';
            }
            else {
                return '****  ****  ****  ' + self.last_four_raw();
            }
        });

        self.trial_active = ko.computed(function() {
            if (self.subscription() && self.subscription().status == 'trialing') {
                return true;
            } else {
                return false;
            }
        });

        self.trial_end = ko.computed(function() {
            if ( self.trial_active() ) {
                d = new Date(0);
                d.setUTCSeconds(self.subscription().trial_end);
                return d.toDateString();
            } else {
                return null;
            }
        });

        self.sponsor_end = ko.computed(function() {
            if ( self.sponsored() ) {
                d = new Date(0);
                d.setUTCSeconds(self.subscription().discount.end);
                return d.toDateString();
            } else {
                return null;
            }
        });

        self.profileActive = ko.computed(function() {
            if (self.content_type() == 'user' && !self.newContent() ) {
                return true;
            } else {
                return false;
            }
        });

        self.updateCustomer = function () {
            $.get('/api/customer', function(response) {
                if (response.customer) {
                    if (response.customer.cards.total_count > 0) {
                        self.last_four_raw(response.customer.cards.data[0].last4);
                    } else {
                        self.last_four_raw(false);
                    }
                    self.subscription(response.customer.subscriptions.data[0]);  
                }
            }).done( function () {
                self.customer_loaded(true);
            });
        };  

        self.newButtonText = ko.computed( function() {
            return 'new ' + self.child_content_type();
        });

        self.initNewContent = function() {
            self.content_title('');
            self.content_description('');
            if (self.child_content_type() == 'lesson') {
                self.initNewLesson();
            }
            else {
                self.newContent(true);
                $("#new-content-div").show();
                self.lessonMode(false);
            }
        };

        self.initNewLesson = function() {
            self.current_lesson_body('');
            self.content_type('lesson');
            self.newContent(null);
            self.lessonMode(true);
            self.current_lesson_id(null);
        };


        self.saveNewContent = function() {
            var body = self.content_description();
            var content_type = self.child_content_type();
            if (self.content_type() == 'lesson') {
                content_type = 'lesson';
            }
            if (content_type == 'lesson') {
                body = self.current_lesson_body();
            }
            var data = {
                title : self.content_title(),
                body : body,
                content_type : content_type,
                course : self.current_course_id(),
                unit: self.current_unit_id(),
            };
            $.post('/api/curriculum', data, function (response) {
                self.fetchAndUpdateContent(response);
            });
            self.newContent(null);
            self.content_type(content_type);
        };

        self.saveLesson = function() {
            if (self.current_lesson_id() == null) {
                self.saveNewContent();
                self.contentChangesDetected(false);
            }
            else {
                var data = {
                    body : self.current_lesson_body(),
                    content_type : 'lesson',
                };
                var url = '/api/curriculum/' + self.current_lesson_id();
                $.post(url, data, function (response) {
                    self.fetchAndUpdateContent(response);
                    self.contentChangesDetected(false);
                });
            }
        };

        self.saveChangesToContent = function() {
            if ( self.content_type() == 'course' ) {
                passphrase = self.course_passphrase();
            } else {
                passphrase = '';
            }

            var data = {
                title : self.content_title(),
                body : self.content_description(),
                content_type : self.content_type(),
                passphrase : passphrase
            };
            var url = '/api/curriculum/' + self.content_id();
            $.post(url, data, function (response) {
                self.fetchAndUpdateContent(response);
                self.contentChangesDetected(false);
            });
        };

        self.updateCourseUnits = function(course_id) {
            var url = '/api/curriculum/' + course_id;
            $.getJSON(url, function (response) {
                self.current_units(response.units);
            });
        };

        self.updateUnitLessons = function(unit_id) {
            var url = '/api/curriculum/' + unit_id;
            $.getJSON(url, function (response) {
                self.current_lessons(response.lessons);
            });
        };

        self.saveChangesToTeacher = function() {
            var data = {
                formalName : self.teacher_name(),
                bio : self.teacher_bio(),
                plan : self.plan(),
            }
            $.ajax({
                url:  '/api/users/' + self.teacher_id(),
                type: 'PUT', 
                data: data, 
                success: function(response) {
                    // something on success maybe?
                },
                fail: function(response) {
                    // you failure!
                }
            }).done(function () {
                self.profileChangesDetected(false);
            });
        };

        self.profileChange = function() {
            self.profileChangesDetected(true);
            return true;
        };

        self.lessonChange = function() {
            self.contentChangesDetected(true);
            return true;
        };

        self.contentChange = function() {
            self.contentChangesDetected(true);
            return true;
        };

        self.fetchAndUpdateContent = function(response) {
            var content_type = response.content_type;
            if (content_type == 'course') {
                self.fetchCourse(response);
            }
            else if (content_type == 'unit') {
                self.fetchUnit(response);
                self.updateCourseUnits(response.content.course);

            }
            else if (content_type == 'lesson') {
                self.fetchLesson(response);
                self.updateUnitLessons(response.content.unit);

            }
            // wait 1 second for NDB consistency, then update
            setTimeout(function() {
                self.updateTeacher();
            }, 1000);
        };
    };
});