'use strict';

let $ = require('jquery');
//hack jquery into window fixes double jquery import issue.
window.jQuery = window.$ = $;


$(document).ready(function () {
  require('donations');  
});

