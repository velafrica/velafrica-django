if ($('span.tracking-date').length) {
  $(".tracking-date:first").addClass("no-before");
  $.each($('span.tracking-date'), function (index, value) {
    var timestamp = $(value).data('date');
    var today = new Date();
    var today_timestamp = today.getMonth() + 1 + '/' + today.getDate() + '/' + today.getFullYear();
    var yesterday = new Date(today.setDate(today.getDate() - 1));
    var next_day_timestamp = yesterday.getMonth() + 1 + '/' + yesterday.getDate() + '/' + yesterday.getFullYear();
    if (timestamp == today_timestamp) {
      $(value).html('Heute');
    } else if (timestamp == next_day_timestamp) {
      $(value).html('Gestern');
    }
  })
}

if($('#tracking-navi').length) {
  $(window).scroll(onScroll);

    //jQuery for page scrolling feature - requires jQuery Easing plugin
    $(function () {
      $('a.page-scroll').bind('click', function (event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
          scrollTop: $($anchor.attr('href')).offset().top
        }, 700, 'easeInOutExpo');
        event.preventDefault();
      });
    });

    function onScroll() {
      var scrollPos = $(document).scrollTop();
      $('#menu-center a').each(function () {
        var currLink = $(this);
        var refElement = $(currLink.attr("href"));
        var heightAnchor = 140;
        if (refElement.position().top - heightAnchor <= scrollPos && refElement.position().top + refElement.height() > scrollPos + heightAnchor) {
          currLink.addClass("active");
        }
        else {
          currLink.removeClass("active");
        }
      });
    }
}
