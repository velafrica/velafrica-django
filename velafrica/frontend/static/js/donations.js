// only load this piece of code if we're on the donation page
if ($('#donation').length) {

  // set the values for paypal and payment slip
  var changeAmount = function(amount) {
    // update the hidden field used for redirecting to paypal
    $('#id_amount').val(amount);

    // update the amount for generating a payment slip
    $('#id_donation_amount').val(amount);
  };

  var emptyAndReadOnly = function() {
    var checkbox = $(this);
    var donation_amount = $('#id_donation_amount');
    if(checkbox.is(':checked')) {
      donation_amount.val(0);
      donation_amount.attr('readonly', true);

    } else {
      donation_amount.attr('readonly', false);
      donation_amount.val($('#md-amounts-tabs li.active a').data('amount'));
    }
  };

  // set the custom donation value after every change of the input form
  $('#custom-amount').change(function(e) {
    var customAmount = $(this);
    customAmount
      .closest('.md-amount-panel')
      .data('amount', customAmount.val());
    changeAmount(customAmount.val());
  });

  // select a predefined value; and update the paypal & payment slip with the donation value
  $('.md-amount-panel').click(function(e) {
    var amountPanel = $(this);
    changeAmount(amountPanel.data('amount'));
    $('.md-amount-panel.active').removeClass('active');
    amountPanel.addClass('active');
  });

  // set the initial value for paypal and the payment slip
  changeAmount($('.md-amount-panel.active').first().data('amount'));

  // disable the amount value if the donor would like an empty payment slip
  $('#id_empty_invoice').change(emptyAndReadOnly);

  // extract and set the redirect_url where the donor will be redirected to after donating money
  $('#id_invoice_redirect_url').val($('#invoice_redirect_url').val());
}

