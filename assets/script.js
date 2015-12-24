// Release Filters
function do_filters() {
  var regex = new RegExp($('.js-text-filter').val(), "i");
  var rows = $('.js-release');
  var type = $('.js-type-filter').val();
  rows.each(function (index) {
    title = $(this).children(".js-title").html()
    if (title.search(regex) != -1 && (type == '0' || $(this).hasClass("js-release-type-" + type))) {
      $(this).show();
    } else {
      $(this).hide();
    }
  });
}

$('.js-type-filter').change(function() {
  do_filters();
})

$('.js-text-filter').keyup(function() {
  do_filters();
});

// Fetch
$('.js-download').click(function() {
  $elem = $(this);
  $.get($elem.attr('href'), function( data ) {
    $elem.replaceWith(data);
  });
  return false;
});

// Artist Info
$('.js-desc-more-link').click(function() {
  $('.js-artist-desc').css('max-height', 'none');
  $('.js-desc-less-link').show();
  $(this).hide();
  return false;
});

$('.js-desc-less-link').click(function() {
  $('.js-artist-desc').css('max-height', '190px');
  $('.js-desc-more-link').show();
  $(this).hide();
  return false;
});

// Release Info
$('.js-more-info').click(function() {
  $elem = $(this);
  group_id = $elem.attr('groupId');
  if (!$.trim( $('.js-more-info-' + $elem.attr('groupId')).html() ).length) {
    $.get($elem.attr('href'), function( data ) {
      $('.js-more-info-' + $elem.attr('groupId')).html(data);
    });
  }
  $elem.hide();
  $('.js-more-info-' + $elem.attr('groupId')).fadeIn();
  $('.js-less-info[groupId=' + group_id + ']').show();
  return false;
});

$('.js-less-info').click(function() {
  $elem = $(this);
  $elem.hide();
  $('.js-more-info[groupId=' + group_id + ']').show();
  $('.js-more-info-' + $elem.attr('groupId')).fadeOut();
  return false;
});
