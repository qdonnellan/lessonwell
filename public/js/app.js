
// Making sure that non-li wrapped buttons that trigger tab events also change the active state
// of related tab-buttons that are wrapped in li divs

$(".unit-home-btn").on("click", function() {
  $('.mobile-lesson-links').removeClass("active");
  $("#unit-overview").parent('li').addClass("active");
});

       
// bootstrap tooptips
$(document).ready(function () {
  $("[rel=tooltip]").tooltip();
});

   
// embedded quizzes
$('.quiz-form').on('submit',function(e){
  e.preventDefault();
  var form = $(this).closest('form');
  $.ajax({
    type: form.attr('method'),
    url: form.attr('action'),
    data: form.serialize()
  }).done(function(the_response) {
    if (the_response === 'true') {
      $(".quiz-reason", form).show();
      $(".correct-answer", form).show();
      $(".incorrect-answer", form).hide();
    }
    else {
      $(".quiz-reason", form).hide();
      $(".correct-answer", form).hide();
      $(".incorrect-answer", form).show();
    };
  });
  return false;
});


// some stuff to handle adding standards to lessons

$('.standard-add').on('submit',function(e){
  e.preventDefault();
  var form = $(this).closest('form');
  $.ajax({
    type: form.attr('method'),
    url: form.attr('action'),
    data: form.serialize(),
    cache: false
              
  }).done(function( the_response ){
    $('#current-standards-div').html(the_response);
    $('#myTab a[href="#current-standards"]').tab('show');          
    $('.standard-add').find('input[type=checkbox]:checked').removeAttr('checked');
  });
  return false;
});


$('#current-standards-div').on('submit','.remove-form',function(e){
  e.preventDefault();
  var form = $(this).closest('form');
  $.ajax({
    type: form.attr('method'),
    url: form.attr('action'),
    data: form.serialize(),
    cache: false,
    success: function(data, status, xHTTP){
      if (data){
        form.remove();
      }
    }
  });
  return false;
});


