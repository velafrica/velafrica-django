// only load this piece of code if we're on the donation page
if ($('.contact_link').length) {
  $('.contact_link').click(function () {
    // tell google analytics about the click
    ga('send', {
      hitType: 'event',
      eventCategory: 'E-Mail',
      eventAction: 'click',
      eventLabel: $(this).attr('href')
    });
  });
}
