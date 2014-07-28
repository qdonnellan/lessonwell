define(
    ['knockout', 'jquery', 'formatLesson', 'highlight'], 
    function (ko, $, formatLesson, hljs) {

    return function viewModel() {
        var self = this;

        self.content_type = ko.observable('user');
        self.content_id = ko.observable(null);
        self.content_title = ko.observable('');
        self.content_description = ko.observable('');

        self.current_course_title = ko.observable('');
        self.current_course_description = ko.observable('');
        self.current_course_id = ko.observable('');
        self.current_units = ko.observableArray([]);
        self.current_unit_title = ko.observable('');
        self.current_unit_description = ko.observable('');
        self.current_unit_id = ko.observable('');
        self.current_lessons = ko.observableArray([]);
        self.current_lesson_title = ko.observable('');
        self.current_lesson_body = ko.observable('');
        self.current_lesson_id = ko.observable(null);

        self.teacher_name = ko.observable('');
        self.teacher_bio = ko.observable('');
        self.teacher_username = ko.observable('');
        self.teacher_id = ko.observable('');
        self.teacher_courses = ko.observableArray([]);

        self.newContent = ko.observable(null);
        self.profileChangesDetected = ko.observable(false);
        self.contentChangesDetected = ko.observable(false);
        self.lessonMode = ko.observable(false);

        self.subscription = ko.observable(null);
        self.last_four_raw = ko.observable(null);

        self.teacher_name_computed = ko.computed(function () {
            if ( self.teacher_name() ) {
                return self.teacher_name();
            } else {
                return self.teacher_username();
            }
        });


        // helpers for absence/presence of content
        self.no_courses = ko.computed(function () {
            var count = 0;
            for ( x in self.teacher_courses() ) { count += 1 }
            if (count == 0) { return true } else { return false }
        });

        self.no_units = ko.computed(function () {
            var count = 0;
            for ( x in self.current_units() ) { count += 1 }
            if (count == 0) { return true } else { return false }
        });

        self.no_lessons = ko.computed(function () {
            var count = 0;
            for ( x in self.current_lessons() ) { count += 1 }
            if (count == 0) { return true } else { return false }
        });


        self.getParameterByName = function(name) {
            name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
            var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
                results = regex.exec(location.search);
            return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
        };

        self.refreshOutputStyle = function() {
            MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
            $('pre code').each(function(i, e) {hljs.highlightBlock(e)});
        };
                
        self.editButtonLink = ko.computed(function() {
            if (self.content_id()) {
                return '/edit?curriculum_id=' + self.content_id();
            } else {
                return '/edit'
            }
        });

        self.publicViewLink = ko.computed(function() {
            if (self.content_id()) {
                return '/' + self.teacher_username() + '?curriculum_id=' + self.content_id();
            } else {
                return '/' + self.teacher_username();
            }
        })

        self.lessonActive = ko.computed(function() {
            if (self.content_type() == 'lesson') {return true;}
            else {return false}
        });

        self.unitActive = ko.computed(function() {
            if (self.lessonActive()) {return true}
            else if (self.content_type() == 'unit') {return true}
            else {return false}
        });

        self.courseActive = ko.computed(function() {
            if (self.lessonActive() || self.unitActive()) {return true}
            else if (self.content_type() == 'course') {return true}
            else {return false}
        });

        self.child_content_type = ko.computed(function() {
            if (self.content_type() == 'course') { return 'unit'}
            else if (self.content_type() == 'unit') {return 'lesson'}
            else if (self.content_type() == 'lesson') {return null}
            else {return 'course'}
        });

        self.formatted_lesson = ko.computed(function() {
            var input_str = self.current_lesson_body();
            return formatLesson.formatInput(input_str);
        }).extend({ notify: 'always' });

        self.activateTab = function(tab) {
            $('#curriculum-tabs').find('li').removeClass('active');
            var tab_id = "#" + tab + '-tab';
            $(tab_id).addClass('active');
        };

        self.userButtonClicked = function() {
            self.content_type('user');
            self.content_id(null);
            self.activateTab('user');
            self.newContent(null);
            self.lessonMode(false);
            self.contentChangesDetected(false);
        };

        self.courseButtonClicked = function() {
            self.content_type('course');
            self.content_id(self.current_course_id());
            self.content_title(self.current_course_title());
            self.content_description(self.current_course_description());
            self.activateTab('course');
            self.newContent(null);
            self.lessonMode(false);
            self.contentChangesDetected(false);
        };

        self.unitButtonClicked = function() {
            self.content_type('unit');
            self.content_id(self.current_unit_id());
            self.content_title(self.current_unit_title());
            self.content_description(self.current_unit_description());
            self.activateTab('unit');
            self.newContent(null);
            self.lessonMode(false);
            self.contentChangesDetected(false);
        };

        self.lessonButtonClicked = function() {
            self.content_type('lesson');
            self.content_id(self.current_lesson_id());
            self.activateTab('unit');
            self.newContent(null);
            self.lessonMode(true);
            self.contentChangesDetected(false);
        };

        self.fetchCourse = function(course) {
            $.getJSON('/api/curriculum/' + course.id, function (response) {
                self.populateCurrentCourse(response);
            }).done(function () {
                self.courseButtonClicked();
            });
        };

        self.populateCurrentCourse = function(response_object) {
            self.current_course_title(response_object.content.title);
            self.current_course_description(response_object.content.body);
            self.current_course_id(response_object.id);
            self.current_units(response_object.units);
            self.content_title(response_object.content.title);
            self.content_description(response_object.content.body);x
        };

        self.fetchUnit = function(unit) {
            $.getJSON('/api/curriculum/' + unit.id, function (response) {
                self.populateCurrentUnit(response);
            }).done(function () {
                self.unitButtonClicked();
            }); 
        };

        self.populateContent = function(content_object, content_type) {
            if ( content_type == 'lesson' ) {
                self.populateCurrentLesson(content_object);
            } else if ( content_type == 'unit' ) {
                self.populateCurrentUnit(content_object);
            } else if ( content_type == 'course' ) {
                self.populateCurrentCourse(content_object);
            }
        }
        self.fetchContentById = function(content_id, content_type) {
            $.getJSON('/api/curriculum/' + content_id, function (response) {
                self.populateContent(response, content_type);
            });
        };

        self.populateCurrentUnit = function(response_object) {
            self.current_unit_title(response_object.content.title);
            self.current_unit_id(response_object.id);
            self.current_unit_description(response_object.content.body);
            self.current_lessons(response_object.lessons);
        };

        self.fetchLesson = function(lesson) {
            $.getJSON('/api/curriculum/' + lesson.id, function (response) {
                self.populateCurrentLesson(response);
            }).done(function () {
                self.lessonButtonClicked();
            }).done(function() {
                self.refreshOutputStyle();
            });
        };

        self.populateCurrentLesson = function(response_object) {
            self.current_lesson_title(response_object.content.title);
            self.current_lesson_body(response_object.content.body);
            self.current_lesson_id(response_object.id);
            self.refreshOutputStyle();
        };

        self.updateTeacher = function() {
            var teacher_data = $('#teacher-data').data();
            var teacher = teacher_data.teacher;
            var teacher_id = teacher_data.teacherid;
            self.teacher_id(teacher_id);
            url = '/api/users/' + teacher_id;
            $.getJSON(url, function (response){
                self.teacher_courses(response.courses);
                self.teacher_name(response.formal_name);
                self.teacher_bio(response.bio);
                self.teacher_username(response.username);
            }).done(function(){
                $(".loading-page").hide();
                $(".content-page").show();
            });
        };

        self.activateSpecificContent = function() {
            var curriculum_id = self.getParameterByName('curriculum_id');
            self.newContent(null);
            if (curriculum_id) {
                var url = '/api/curriculum/' + curriculum_id;
                $.getJSON(url, function (response) {
                    if (response.content_type == 'lesson') {
                        self.fetchContentById(response.content.course, 'course');
                        self.fetchContentById(response.content.unit, 'unit');
                        self.populateCurrentLesson(response);
                        self.lessonButtonClicked();
                    } else if (response.content_type == 'unit') {
                        self.fetchContentById(response.content.course, 'course');
                        self.populateCurrentUnit(response);
                        self.unitButtonClicked();
                    } else if (response.content_type == 'course') {
                        self.populateCurrentCourse(response);
                        self.courseButtonClicked();
                    }
                }).fail(function() {
                    // do something on failure
                }).done(function() {
                    self.updateTeacher();
                }).done(function() {
                    self.refreshOutputStyle();
                });
            } else {
                self.updateTeacher();
            }
        };
    };
});

