$(function() {

    alert = $("#alert_box");

    var show_alert = function(msg) {
        alert.find("#alert_content").html(msg);
        alert.toggleClass('hidden show');
        setTimeout(function() { alert.toggleClass('hidden show') }, 5000);
    }

    form = $("#find_form");
    table = $("#result_table");

    row_template = $("<tr></tr>");

    var update = function() {
        table.empty();

        out_data = $(form).serialize();

        $.get('/list_poi/', out_data, function(data, status) {

            if (status == 'success') {

                if (!data['error']) {
                    for (var i = 0; i < data['result'].length; i++) {
                        obj = data['result'][i];

                        row = row_template.clone();

                        row.append( $("<td></td>").html(obj['name']) );
                        row.append( $("<td></td>").html(obj['x']) );
                        row.append( $("<td></td>").html(obj['y']) );

                        table.append(row);
                    }
                } else {
                    show_alert(data['msg']);
                }

            } else {
                show_alert('An error occurred during the request. Please try again.');
            }

        });
    };

    form.on('submit', function(evt) {
        evt.preventDefault();
        update();
    });

    update();
});
