function ViewModel() {
    var self = this;
    self.sandboxInput = ko.observable('');
    self.content_type = ko.observable(null);
    self.newContent = ko.observable(false);
    self.courseButtonDisabled = ko.observable('');
    self.content_title = ko.observable('');
    self.content_description = ko.observable('');
    self.teacher_courses = ko.observableArray([]);
    self.current_course_title = ko.observable('');
    self.current_course_id = ko.observable('');
    self.current_units = ko.observableArray([]);
    self.current_unit_title = ko.observable('');
    self.current_unit_id = ko.observable('');
    self.current_lessons = ko.observableArray([]);

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
    self.sandboxOutput = ko.computed(function() {
        var input_str = self.sandboxInput();
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
    };

    self.courseButtonClicked = function() {
        self.content_type('course');
        self.newContent(false);
    };

    self.unitButtonClicked = function() {
        self.content_type('unit');
        self.newContent(false);
    };

    self.lessonButtonClicked = function() {
        self.content_type('lesson');
        self.newContent(false);
    };

    self.initNewContent = function() {
        self.content_title('');
        self.content_description('');
        self.newContent(true);
        self.courseButtonDisabled = ko.observable('disabled');
    };

    self.initNewLesson = function() {
        self.sandboxInput('');
        self.content_type('lesson');
        self.newContent(true);
    }

    self.fetchCourse = function(course) {
        var url = '/api/curriculum/' + course.id
        $.getJSON(url, function (response) {
            self.current_course_title(response.content.title);
            self.current_course_id(response.id);
            self.current_units(response.units);
            self.courseButtonClicked() 
        });
    };

    self.fetchUnit = function(unit) {
        var url = '/api/curriculum/' + unit.id
        $.getJSON(url, function (response) {
            self.current_unit_title(response.content.title);
            self.current_unit_id(response.id);
            self.current_lessons(response.lessons);
            self.unitButtonClicked() 
        });
    };

    self.saveNewContent = function() {
        var data = {
            title : self.content_title(),
            body : self.content_description(),
            content_type : self.child_content_type(),
            course : self.current_course_id(),
        };
        $.post('/api/curriculum', data, function (response) {
            if (data.content_type == 'course') {
                self.fetchCourse(response);
            }
            else if (data.content_type == 'unit') {
                self.fetchUnit(response);
            }
            self.updateTeacherCourses();
        });
        self.newContent(false);
        self.content_type(self.child_content_type());
    };

    self.updateTeacherCourses = function() {
        $.getJSON('/api/user', function (response){
            vm.teacher_courses(response.courses);
        });
    };
};

// make sure mathjax is called after each new character input
// in the text area; displays math real time
$("#sandbox-textarea").on('keyup', function () {
    setTimeout(refreshOutputStyle, 1000);
});

function refreshOutputStyle() {
    MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
    $('pre code').each(function(i, e) {hljs.highlightBlock(e)});
};

vm = new ViewModel();
ko.applyBindings(vm);

$(document).ready(function() {
    vm.updateTeacherCourses();
});




