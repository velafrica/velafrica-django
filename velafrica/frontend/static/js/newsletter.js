if ($('#newsletter-form').length) {
  $('#newsletter-form').submit(function (event) {
    event.preventDefault();
    if ($(this).find('input[name="email"]').val() != '') {
      var data = $(this).serialize();
      var buttonVal = $("#newsletter-submit").val();
      $.ajax(
        {
          type: 'POST',
          url: $('#newsletter-subscribe-url').val(),
          data: data
        }
      ).done(function (response) {
        if (response === true) {
          $("#newsletter-submit").css("background-color", "green").val("Abonniert!");
        } else {
          $("#newsletter-submit").css("background-color", "red").val("Fehlgeschlagen!");
        }
        setTimeout(function () {
          $("#newsletter-submit").css("background-color", "").val(buttonVal);
          $("#newsletter-email-field").val("");
        }, 4000);
      })
    } else {
      //TODO: email validation (client)
    }
  });
}
