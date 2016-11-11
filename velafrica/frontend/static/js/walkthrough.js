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
            $('#id_collected_before').val(true);
        }
        if ($(this).attr("value") == "no") {
            $('#id_collected_before_note').hide();
            $('#id_collected_before').val(false);
        }
    });
}
