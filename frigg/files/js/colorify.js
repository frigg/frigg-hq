$(document).ready(function() {
  $('.colorify').each(function() {
    var html = ansi_up.ansi_to_html($(this).html());
    $(this).html(html);
  });
});
