$(document).ready(function() {
    $(".timestamp").each(function() {
        $(this).html(moment(moment.utc($(this).html()).toDate()).format("YYYY-MM-DD HH:mm"));
    })
});
