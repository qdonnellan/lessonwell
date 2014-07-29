define(
    ['knockout', './editContentViewModel', 'jquery', 'rangyinputs', 'qSelect'], 
    function (ko, viewModel, $, rangy, qSelect) {

        var vm = new viewModel();
        ko.applyBindings( vm );

        $(document).ready(function() {
            vm.activateSpecificContent();
            vm.updateCustomer();
        });

        $("#lesson-textarea").on('keyup', function () {
            vm.refreshOutputStyle();
        });

        $(document).ready(function() {
            qSelect( vm );
        });
    });