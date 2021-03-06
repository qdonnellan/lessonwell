define(['knockout'], function (ko, icheck) {

    function viewModel() {
        var self = this;
        self.email = ko.observable('');
        self.email2 = ko.observable('');

        self.email_validated = ko.computed(function() {
            if (!self.email()) {
                return false;
            } else if (self.email2() == self.email() ) {
                return true;
            } else {
                return false;
            }
        });

        self.stripe_script = ko.computed(function() {
            var stripe_data = $('#stripe-data').data();
            var pubkey = stripe_data.pubkey;
            var script_string = '<script \
                src="https://checkout.stripe.com/checkout.js" class="stripe-button" \
                data-key=STRIPE_PUB_KEY \
                data-image="/lessonwell_square.png" \
                data-name="lessonwell" \
                data-email=STRIPE_EMAIL \
                data-panel-label="Sponsor Now" \
                data-description="Multiple Teacher Subscriptions" \
                data-allow-remember-me="true" \
                data-label="Complete Purchase" \
                > \
            </script>';
            script_string = script_string.replace('STRIPE_PUB_KEY', pubkey);
            script_string = script_string.replace('STRIPE_EMAIL', self.email());
            return script_string;
        });

        self.getParameterByName = function(name) {
            name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
            var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
                results = regex.exec(location.search);
            return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
        };

    };

    var vm = new viewModel()
    ko.applyBindings( vm );

    $( document ).ready(function() {
        var sub = vm.getParameterByName("subscriptions");
        
        if ( sub == '5' ) {
            $("#quantity05").prop("checked", true);
        } else if ( sub == '10' ) {
            $("#quantity10").prop("checked", true);
        } else if ( sub == '20' ) {
            $("#quantity20").prop("checked", true);
        }
    });


});

