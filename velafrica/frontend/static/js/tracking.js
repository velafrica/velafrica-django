if ($('span.tracking-date').length) {
  $(".tracking-date:first").addClass("no-before");
  $.each($('span.tracking-date'), function (index, value) {
    var timestamp = $(value).data('date');
    var today = new Date();
    var today_timestamp = today.getMonth() + 1 + '/' + today.getDate() + '/' + today.getFullYear();
    var yesterday = new Date(today.setDate(today.getDate() - 1));
    console.log(yesterday);
    var next_day_timestamp = yesterday.getMonth() + 1 + '/' + yesterday.getDate() + '/' + yesterday.getFullYear();
    console.log(today, yesterday);
    if (timestamp == today_timestamp) {
      $(value).html('Heute');
    } else if (timestamp == next_day_timestamp) {
      $(value).html('Gestern');
    }
  })
}
