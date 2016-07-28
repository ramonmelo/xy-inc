$(function() {

    alert = $("#alert_box");

    form = $("#create_form");

    form.on('submit', function(evt) {
        evt.preventDefault();

        out_data = $(this).serialize();

        $.post('/create_poi/', out_data, function(data, status) {
            alert.removeClass('alert-warning alert-info');

            if (status == 'success') {
                alert.addClass(data['error'] ? 'alert-warning' : 'alert-info');
                alert.find("#alert_content").html(data['msg']);

                if (!data['error']) {
                    form.trigger("reset");
                }

            } else {
                alert.addClass('alert-warning');
                alert.find("#alert_content").html('An error occurred during the request. Please try again.');
            }

            alert.toggleClass('hidden show');
            setTimeout(function() { alert.toggleClass('hidden show') }, 5000);
        });
    });
});
