define(['./baseViewModel', 'knockout'], function (baseViewModel, ko) {
    
    return function profileViewModel() {
        var self = this;
        // profileViewModel inherits from the baseViewModel
        ko.utils.extend( self, new baseViewModel() );

    };
});