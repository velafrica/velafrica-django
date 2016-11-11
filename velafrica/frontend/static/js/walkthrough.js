// only load this piece of code if we're on the donation page
if ($('#walkthrough').length) {

    var toggler = function (divIdButton, divIdToggle) {
        $(divIdToggle)
            .toggle();
        $(divIdButton)
            .find('span')
            .toggleClass('vel-icon arrow-up-white')
            .toggleClass('vel-icon arrow-down-white');
    };

    $('#walkDetail').click(function () {
        toggler('#walkDetail', '#walkDetailInfo');
    });

    $('input[name="optionsRadios"]').click(function () {
        if ($(this).attr("value") == "yes") {
            $('#id_collected_before_note').show();
            $('#id_collected_before').val('True');
        }
        if ($(this).attr("value") == "no") {
            $('#id_collected_before_note').hide();
            $('#id_collected_before').val('False');
        }
    });

    $('input[name="dateRadios"]').click(function() {
        if($(this).attr('value') == 'yes') {
            $('#id_date_fixed').val('True');
            $('#id_date').show();
        }
        if($(this).attr('value') == 'no') {
            $('#id_date_fixed').val('False');
            $('#id_date').hide();
        }
    });

    $('input[name="storeRadios"]').click(function() {
        if($(this).attr('value') == 'yes') {
            $('#id_can_store').val('True');
        }
        if($(this).attr('value') == 'no') {
            $('#id_can_store').val('False');
        }
    });

    $('input[name="deliverRadios"]').click(function() {
        if($(this).attr('value') == 'yes') {
            $('#id_can_deliver').val('True');
        }
        if($(this).attr('value') == 'no') {
            $('#id_can_deliver').val('False');
        }
    });

    $('input[name="vaRadios"]').click(function() {
        if($(this).attr('value') == 'yes') {
            $('#id_velafrica_pickup').val('True');
        }
        if($(this).attr('value') == 'no') {
            $('#id_velafrica_pickup').val('False');
        }
    });
}
