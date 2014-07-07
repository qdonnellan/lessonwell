define(
    ['knockout', './editContentViewModel', 'jquery'], 
    function (ko, viewModel, $) {

    var vm = new viewModel()
    ko.applyBindings( vm );

    $(document).ready(function() {
        vm.activateSpecificContent();
        vm.updateCustomer();
    });

    $("#lesson-textarea").on('keyup', function () {
        vm.refreshOutputStyle();
    });


});

