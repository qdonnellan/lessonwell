function ViewModel() {
    var self = this;
    self.server_msg = ko.observable()
    self.username = ko.observable('');
    self.error_msg = ko.computed(function() {
        if (self.username().length < 5) {
            return 'username is too short; must be at least 5 characters';
        }
        else if (self.username().length > 20) {
            return 'username is too long; may be no longer than 20 characters';
        }
        else if ((/^\w+$/.test(self.username())) != true) {
            return 'username may only contain letters and numbers';
        }
        else {
            return false
        }
    });
    self.has_error = ko.computed(function() {
        if (self.error_msg()) {return true;}
        else {return false;}
    });
    self.has_success = ko.computed(function() {
        if (self.error_msg()) {return false;}
        else {return true;}
    });
};

vm = new ViewModel();
ko.applyBindings(vm);


