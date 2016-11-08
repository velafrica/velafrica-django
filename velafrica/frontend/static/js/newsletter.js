if ($('#newsletter-form').length) {
  $('#newsletter-form').submit(function (event) {
    event.preventDefault();
    if ($(this).find('input[name="email"]').val() != '') {
      var data = $(this).serialize();
      $.ajax(
          {
            type: 'POST',
            url: $('#newsletter-subscribe-url').val(),
            data: data
          }
      ).done(function (response) {
        console.log(response);
      })
    } else {
      //TODO: email validation (client)
    }
  });
}
