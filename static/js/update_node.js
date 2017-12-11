var submitForm = function(){
    document.getElementById("data_set").value = "My value";
    $("#data_set").val("My value");
    $('.js_save_button').fadeIn();
//  var email = $("form input[name='email']").val(),
//      amount = $("form input[name='amount']").val();
//  $.ajax({
//    method: 'POST',
//    url: '/submit_order/',
//    data: JSON.stringify({
//      email: email,
//      amount: amount,
//      product_id: {{ object.pk }}
//    })
  }).done(function(msg){
//    console.log(msg);
//    $('form').hide();
//    $('.js_data_set').text("test");
//    $('.success_order').fadeIn();
    document.getElementById("data_set").value = "My value";
    $("#data_set").val("My value");
    $('.js_save_button').fadeIn();
  });
};
$('.js_save_button').click(function(e){
    document.getElementById("data_set").value = "My value";
    $("#data_set").val("My value");
    $('.js_save_button').fadeIn();
  e.preventDefault();
  submitForm();
});