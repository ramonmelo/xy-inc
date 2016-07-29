$(function() {

    alert = $("#alert_box");

    var show_alert = function(msg) {
        alert.find("#alert_content").html(msg);
        alert.toggleClass('hidden show');
        setTimeout(function() { alert.toggleClass('hidden show') }, 5000);
    }

    form = $("#create_form");

    form.on('submit', function(evt) {
        evt.preventDefault();

        out_data = $(this).serialize();

        $.post('/create_poi/', out_data, function(data, status) {
            alert.removeClass('alert-warning alert-info');

            if (status == 'success') {
                alert.addClass(data['error'] ? 'alert-warning' : 'alert-info');
                show_alert(data['msg']);

                if (!data['error']) {
                    form.trigger("reset");
                }

            } else {
                alert.addClass('alert-warning');
                show_alert('An error occurred during the request. Please try again.');
            }
        });
    });
});
