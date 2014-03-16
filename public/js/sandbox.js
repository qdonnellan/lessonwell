function ViewModel() {
    var self = this;
    self.sandboxInput = ko.observable('');
    self.sandboxOutput = ko.computed(function() {
        var input_str = self.sandboxInput();
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


