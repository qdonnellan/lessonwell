function ViewModel() {
    var self = this;

    self.content_type = ko.observable('user');
    self.content_id = ko.observable(null);
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
    self.teacher_name = ko.observable('');
    self.teacher_bio = ko.observable('');

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
        // requires 'format.js'
        return formatInput(input_str);
    });

    self.userButtonClicked = function() {
        self.content_type('user');
        self.content_id(null);
    };

    self.courseButtonClicked = function() {
        self.content_type('course');
        self.content_id(self.current_course_id());
    };

    self.unitButtonClicked = function() {
        self.content_type('unit');
        self.content_id(self.current_unit_id());
    };

    self.lessonButtonClicked = function() {
        self.content_type('lesson');
        self.content_id(self.current_lesson_id());
    };

    self.fetchCourse = function(course) {
        var url = '/api/curriculum/' + course.id;
        $.getJSON(url, function (response) {
            self.current_course_title(response.content.title);
            self.current_course_description(response.content.body);
            self.current_course_id(response.id);
            self.current_units(response.units);
            self.courseButtonClicked()
        });
    };

    self.fetchUnit = function(unit) {
        var url = '/api/curriculum/' + unit.id;
        $.getJSON(url, function (response) {
            self.current_unit_title(response.content.title);
            self.current_unit_id(response.id);
            self.current_unit_description(response.content.body);
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
            self.lessonButtonClicked()
            refreshOutputStyle();
        });
    };

    self.updateTeacher = function() {
        $.getJSON('/api/user', function (response){
            self.teacher_courses(response.courses);
            self.teacher_name(response.formal_name);
            self.teacher_bio(response.bio);
        });
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
    refreshOutputStyle();
});
