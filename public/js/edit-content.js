function ViewModel() {
    var self = this;
    self.sandboxInput = ko.observable('');
    self.content_type = ko.observable(null);
    self.newContent = ko.observable(false);
    self.courseButtonDisabled = ko.observable('');
    self.content_title = ko.observable('');
    self.content_description = ko.observable('');

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
        self.sandboxInput('');
        self.newContent(true);
        self.courseButtonDisabled = ko.observable('disabled');
    };

    self.saveNewContent = function() {
        data = {
            title : self.content_title(),
            body : self.content_description(),
        }
        url = '/' + self.child_content_type()
        $.post(url, data, function() {
            // do something with the response maybe?
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




