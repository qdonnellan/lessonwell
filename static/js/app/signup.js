define(['knockout'], function (ko) {

    function viewModel() {
        var self = this;
        self.server_msg = ko.observable(null)
        self.username = ko.observable('');
        self.formal_name = ko.observable('');
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

        self.toggle_loading_button = function(option) {
            if (option == 'on') {
                $('.btn-loading-text').show();
                $('.btn-waiting-text').hide();
                $('#create-account-btn').prop('disabled', true);
            } else if (option == 'off') {
                $('.btn-loading-text').hide();
                $('.btn-waiting-text').show();
                $('#create-account-btn').prop('disabled', false);
            }
        }

        self.createAccount = function () {
            self.toggle_loading_button('on');
            self.server_msg(null);
            var data = {
                formalName : self.formal_name(),
                username : self.username(),
            };
            $.post('/api/users', data, function (response) {
                if ('error' in response) {
                    self.server_msg(response['error']);
                } else if ('success' in response) {
                    window.location.replace('/success')
                }
            }).done( function () {
                self.toggle_loading_button('off');
            });

        }
    };

    var vm = new viewModel()
    ko.applyBindings( vm );

    $(document).ready(function() {
        $(".loading-page").hide();
        $(".signup-page").show();
    });
});

