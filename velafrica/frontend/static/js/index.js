if ($('#tracking-code-form').length) {
  $('#tracking-code-form').submit(function(event) {
    event.preventDefault();
    var trackingInput = $(this).find('input[class="tracking-code"]');
    if (trackingInput.val() != '') {
      window.location.href = '/my-tracking/' + trackingInput.val();
    } else {
      //TODO: whatever velafrica wants to happen when no tracking code was entered
    }
  })
}
