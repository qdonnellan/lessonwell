function ViewModel() {
    var self = this;

    self.teacher_id = ko.observable('');
    self.content_type = ko.observable(null);
    self.newContent = ko.observable(false);
    self.content_id = ko.observable('');
    self.content_title = ko.observable('');
    self.content_description = ko.observable('');
    self.teacher_courses = ko.observableArray([]);
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
    self.formal_name = ko.observable('');
    self.profileChangesDetected = ko.observable(false);
    self.contentChangesDetected = ko.observable(false);
    self.bio = ko.observable('');
    self.plan = ko.observable('');
    self.lessonMode = ko.observable(false);
    self.last_four_raw = ko.observable(null);
    self.last_four = ko.computed(function() {
        if (!self.last_four_raw()) {
            return 'loading...';
        }
        else {
            return '****  ****  ****  ' + self.last_four_raw();
        }
    });

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

    self.newButtonText = ko.computed(function() {
        return 'new ' + self.child_content_type();
    })
    self.formatted_lesson = ko.computed(function() {
        var input_str = self.current_lesson_body();
        // requires 'format.js'
        return formatInput(input_str);
    });

    self.currentGif = ko.observable('/img/instructional_gifs/headers.gif')

    // each instructional gif should be 800 x 400 (or the same ratio, 2 x 1)
    self.instructionalGifs = ko.observableArray([
        {
            'name':'Headers',
            'link': '/img/instructional_gifs/headers.gif',
        },
        {
            'name':'Lists',
            'link': '/img/instructional_gifs/lists.gif'
        },
        {
            'name':'Bold/Italic',
            'link': ''
        },
        {
            'name':'Youtube',
            'link': ''
        },

    ]);

    self.setCurrentImage = function(gifInfo) {
        self.currentGif(gifInfo.link);
    };

    self.editButtonClicked = function() {
        self.content_type(null);
        self.newContent(false);
        self.lessonMode(false);
        self.contentChangesDetected(false);
    };

    self.courseButtonClicked = function() {
        self.content_type('course');
        self.content_title(self.current_course_title());
        self.content_description(self.current_course_description());
        self.content_id(self.current_course_id());
        self.newContent(false);
        self.lessonMode(false);
        self.contentChangesDetected(false);
    };

    self.unitButtonClicked = function() {
        self.content_type('unit');
        self.content_title(self.current_unit_title());
        self.content_description(self.current_unit_description());
        self.content_id(self.current_unit_id());
        self.newContent(false);
        self.lessonMode(false);
        self.contentChangesDetected(false);
    };

    self.lessonButtonClicked = function() {
        self.content_type('lesson');
        self.newContent(false);
        self.lessonMode(true);
        self.contentChangesDetected(false);
    };

    self.initNewContent = function() {
        self.content_title('');
        self.content_description('');
        if (self.child_content_type() == 'lesson') {
            self.initNewLesson();
        }
        else {
            self.newContent(true);
            self.lessonMode(false);
        }
    };

    self.initNewLesson = function() {
        self.current_lesson_body('');
        self.content_type('lesson');
        self.newContent(false);
        self.lessonMode(true);
        self.current_lesson_id(null);
    }

    self.fetchCourse = function(course) {
        var url = '/api/curriculum/' + course.id;
        $.getJSON(url, function (response) {
            self.current_course_title(response.content.title);
            self.content_title(response.content.title);
            self.current_course_description(response.content.body);
            self.content_description(response.content.body);
            self.current_course_id(response.id);
            self.current_units(response.units);
            self.courseButtonClicked()
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

    self.fetchUnit = function(unit) {
        var url = '/api/curriculum/' + unit.id;
        $.getJSON(url, function (response) {
            self.current_unit_title(response.content.title);
            self.current_unit_id(response.id);
            self.current_unit_description(response.content.body);
            self.content_description(response.content.body);
            self.current_lessons(response.lessons);
            self.unitButtonClicked()
        });
    };

    self.fetchLesson = function(lesson) {
        var url = '/api/curriculum/' + lesson.id;
        $.getJSON(url, function (response) {
            self.current_lesson_title(response.content.title);
            self.current_lesson_body(response.content.body);
            self.current_lesson_id(response.id);
            self.lessonMode(true);
            self.newContent(false);
            self.content_type('lesson');
            refreshOutputStyle();
        });
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
        self.newContent(false);
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
        var data = {
            title : self.content_title(),
            body : self.content_description(),
            content_type : self.content_type(),
        };
        var url = '/api/curriculum/' + self.content_id();
        $.post(url, data, function (response) {
            self.fetchAndUpdateContent(response);
            self.contentChangesDetected(false);
        });
    };

    self.updateTeacher = function() {
        var teacher_data = $('#teacher-data').data();
        var teacher = teacher_data.teacher;
        self.teacher_id(teacher_data.teacherid);
        var url = '/api/users/' + self.teacher_id;
        $.getJSON(url, function (response){
            self.teacher_courses(response.courses);
            self.formal_name(teacher.formalName);
            self.bio(teacher.bio);
        });
    };

    self.saveChangesToTeacher = function() {
        var data = {
            formalName : self.formal_name(),
            bio : self.bio(),
            plan : self.plan(),
        }
        $.ajax({
            url:  '/api/users/' + self.teacher_id(),
            type: 'PUT', 
            data: data, 
            success: function(response) {
                //something should probably go here...
            }
        });
    };

    self.updateCard = function() {
        $.getJSON('/api/card', function (response){
            self.last_four_raw(response.last4);
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

// make sure mathjax is called after each new character input
// in the text area; displays math real time
$("#lesson-textarea").on('keyup', function () {
    setTimeout(refreshOutputStyle(), 1000);
});

function refreshOutputStyle() {
    MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
    $('pre code').each(function(i, e) {hljs.highlightBlock(e)});
};

vm = new ViewModel();
ko.applyBindings(vm);

$(document).ready(function() {
    vm.updateTeacher();
    vm.updateCard();
    refreshOutputStyle();
});
