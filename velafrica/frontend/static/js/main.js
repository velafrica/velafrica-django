'use strict';

var $ = require('jquery');
//hack jquery into window fixes double jquery import issue.
window.jQuery = window.$ = $;
require('jquery-easing');

window.getUrlVars = function () {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

window.formatDate = function (date) {
    var slices = date.split("-");
    return slices[2] + '.' + slices[1] + '.' + slices[0]
}


$(document).ready(function () {
    require('index');
    require('donations');
    require('bootstrap.min');
    require('map');
    require('contact');
    require('newsletter');
    require('walkthrough');
    require('tracking');
    require('blog');
});


