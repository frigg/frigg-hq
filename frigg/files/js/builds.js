$(document).ready(function() {
    $(".timestamp").each(function() {
        $(this).html(moment(moment.utc("2014-10-10 08:00").toDate()).format("YYYY-MM-DD hh:mm"));
    })
});
