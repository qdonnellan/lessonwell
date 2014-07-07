define(
    ['knockout', './profileViewModel', 'jquery'], 
    function (ko, viewModel, $) {

    var vm = new viewModel()
    ko.applyBindings( vm );

    $(document).ready(function() {
        vm.activateSpecificContent();
    });

    $("#lesson-textarea").on('keyup', function () {
        vm.refreshOutputStyle();
    });

});

