function ViewModel() {
    var self = this;
    self.sandboxInput = ko.observable('')
    self.sandboxOutput = ko.computed(function() {
        return markdown.toHTML(self.sandboxInput());
    });
};

// make sure mathjax is called after each new character input
// in the text area; displays math real time
$("#sandbox-textarea").keyup(function () {
    MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
});

vm = new ViewModel();
ko.applyBindings(vm);


