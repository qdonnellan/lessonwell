define(
    ['knockout', './editContentViewModel', 'jquery', 'qSelect'], 
    function (ko, viewModel, $, qSelect) {

        var vm = new viewModel();
        ko.applyBindings( vm );

        $("#lesson-textarea").on('keyup', function () {
            vm.refreshOutputStyle();
        });

        $(document).ready(function() {
            vm.activateSpecificContent();
            vm.updateCustomer();
            qSelect( vm );
        });
    });

