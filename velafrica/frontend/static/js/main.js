'use strict';

var $ = require('jquery');
//hack jquery into window fixes double jquery import issue.
window.jQuery = window.$ = $;


$(document).ready(function () {
  require('donations');
  require('bootstrap.min');
});

