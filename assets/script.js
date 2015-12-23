$('.js-show-all').click(function() {
  $('.js-release').each(function() {
    $(this).removeClass('u-hidden');
  });
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
    $elem.replaceWith('Fetched!');
  });
  return false;
});
