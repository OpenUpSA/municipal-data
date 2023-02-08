$(() => {
  $iframe = $('.video-chooser iframe');

  $('.video-chooser .video-choices a').on('click', function (e) {
    e.preventDefault();
    var $btn = $(this);
    $btn.closest('.nav').find('li').removeClass('active');
    $btn.closest('li').addClass('active');

    $iframe.attr('src', `${this.href}?autoplay=1`);
    ga('send', 'event', 'play-video', $btn.data('lang'));
    gtag('event', 'play_video', {
      lang: $btn.data('lang'),
    });
  });

  $('#video-modal')
    .on('show.bs.modal', () => {
      var $target = $('.video-chooser .video-choices .active a');
      $iframe.attr('src', `${$target.attr('href')}?autoplay=1`);
      ga('send', 'event', 'play-video', $target.data('lang'));
      gtag('event', 'play_video', {
        lang: $btn.data('lang'),
      });
    })
    .on('hide.bs.modal', () => {
      $iframe.attr('src', '');
    });
});
