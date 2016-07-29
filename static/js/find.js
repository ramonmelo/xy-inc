$(function() {

    form = $("#find_form");
    table = $("#result_table");

    row_template = $("<tr></tr>");

    var update = function() {
        table.empty();

        out_data = $(form).serialize();

        $.get('/list_poi/', out_data, function(data, status) {
            if (!data['error']) {
                for (var i = 0; i < data['result'].length; i++) {
                    obj = data['result'][i];

                    row = row_template.clone();

                    row.append( $("<td></td>").html(obj['name']) );
                    row.append( $("<td></td>").html(obj['x']) );
                    row.append( $("<td></td>").html(obj['y']) );

                    table.append(row);
                }
            }
        });
    };

    form.on('submit', function(evt) {
        evt.preventDefault();
        update();
    });

    update();
});
