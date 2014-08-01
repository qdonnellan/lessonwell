$('.about-open').on('click', function() {
    $('.footer-container').animate({
        height: '300px',
    }, 500);

    $(this).hide();
    $('.about-close').show();
});

$('.about-close').on('click', function() {

    $(this).hide();
    $('.about-open').show();

    $('.footer-container').animate({
        height: '28px'
    }, 500);

    

});