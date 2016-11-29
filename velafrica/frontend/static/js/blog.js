if ($('.blog-list').length) {
  var sizePosts = function () {
    var $posts = $('article.post-item .post_container');

    // reset the hard-set height, so we can get the actual height the element needs
    $posts.height('height', '');

    var highestPostHeight = 0;
    $posts.each(function() {
      var postHeight = $(this).height();
      if (postHeight > highestPostHeight) {
        highestPostHeight = postHeight;
      }
    });

    $posts.css('height', highestPostHeight + 74);
  }
  sizePosts();
}