$('.js-show-all').click(function() {
  $('.js-release').each(function() {
    $(this).removeClass('u-hidden');
  });
  return false;
});

function filter_release_type(release_type) {
  $('.js-release').each(function() {
    if ($(this).hasClass('js-release-type-' + release_type)) {
      $(this).removeClass('u-hidden');
    } else {
      $(this).addClass('u-hidden');
    }
  });
}

function bind_button(type, number) {
  $('.js-only-' + type).click(function() {
    filter_release_type(number);
    return false;
  });
}

bind_button('albums', 1);
bind_button('anthologies', 6);
bind_button('compilations', 7);
bind_button('demos', 23);
bind_button('singles', 9);
bind_button('soundtracks', 3);
bind_button('live', 11);
bind_button('remixes', 13);
bind_button('eps', 5);
bind_button('bootlegs', 14);

$('.js-download').click(function() {
  $elem = $(this);
  $.get($elem.attr('href'), function( data ) {
    $elem.replaceWith(data);
  });
  return false;
});

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
