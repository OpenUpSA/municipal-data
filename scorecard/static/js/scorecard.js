jQuery.support.cors = true;

// attach browser dimensions for help with charts and tables
window.browserWidth = document.documentElement.clientWidth;
window.browserHeight = document.documentElement.clientHeight;

// navigation menu
$('#menu-toggle').on('click', function() {
    $('#menu').slideToggle(150);
});

$(document).ready(function(){
  // prepare ajax spinners
  $('body').append('<div id="body-spinner"></div>');
  var spinnerTarget = document.getElementById('body-spinner'),
      spinner = new Spinner();

  if ($('#profile').length > 0) {
    // profile page stuff

    //Get page-nav offset from top of page
    var pagenavOffset = $('.page-nav-container').offset().top;

    //Affix page-nav to top of page on scroll
    $('.page-nav-container').affix({
      offset: {
        top: pagenavOffset
      }
    });

    //Expand page-nav once affixed
    $('.page-nav-container').on('affixed.bs.affix', function () {
      $('.page-nav-wrapper').addClass('expanded');
    });

    //Un-expand page-nav once nolonger affixed
    $('.page-nav-container').on('affixed-top.bs.affix', function () {
      $('.page-nav-wrapper').removeClass('expanded');
    });

    //Change active tab when scrolling using Bootstrap scrollspy.js
    $('body').scrollspy({ 
      target: '.page-nav-container',
      offset: 100
    });    

    //Easy scrolling (a link to #section will scroll to #section)
    $('.nav a[href^="#"]').on('click',function (e) {
      e.preventDefault();

      var target = this.hash;
      var $target = $(target);

      if ($target.length) {
        $('html, body').stop().animate({
            'scrollTop': $target.offset().top-15
        }, 300, 'swing');
      }
    });

    $('.collapse')
      .on('shown.bs.collapse', function() {
        var $toggle = $('a.show-more[href="#' + this.id + '"]');
        $toggle.find('.fa').removeClass('fa-plus').addClass('fa-minus');
      })
      .on('hidden.bs.collapse', function() {
        var $toggle = $('a.show-more[href="#' + this.id + '"]');
        $toggle.find('.fa').removeClass('fa-minus').addClass('fa-plus');
      });

    //Load video modal
    $('.video-link').click(function(event){
      event.preventDefault();

      var videoTitle = $(this).attr('data-videoTitle');
      $('#video-title').text(videoTitle);

      var videoURL = $(this).attr('data-videoURL');
      $('#video-iframe').attr('src', videoURL);

      var videoURLAfr = $(this).attr('data-videoURLAfr');
      var videoURLZul = $(this).attr('data-videoURLZul');
      var videoURLXho = $(this).attr('data-videoURLXho');

      /* If any of the languages are specified, add a language selection menu to the modal */
      if ( videoURLAfr.length || videoURLZul.length || videoURLXho.length ){
        var languageOptions = ('<ul class="nav nav-pills" id="video-language-menu"><li role="presentation" class="active"><a href="' + videoURL + '" target="video-iframe">English</a></li>');
        if( videoURLAfr.length ) {
          languageOptions += ('<li role="presentation"><a href="' + videoURLAfr + '" target="video-iframe">Afrikaans</a></li>');
        }
        if( videoURLZul.length ) {
          languageOptions += ('<li role="presentation"><a href="' + videoURLZul + '" target="video-iframe">Zulu</a></li>');
        }
        if( videoURLXho.length ) {
          languageOptions += ('<li role="presentation"><a href="' + videoURLXho + '" target="video-iframe">Xhosa</a></li>');
        }
        languageOptions += '</ul>';
        $('#video-modal .modal-body').append(languageOptions);
      }
      $('#video-modal').modal('show');
    });

    $('#video-modal').on('hide.bs.modal', function(){
      $('#video-iframe').attr('src', '');
      $('#video-language-menu').remove();
    });

    //Switch active language nav item when clicked
    $(document).on("click", "#video-language-menu li a", function() {
      $('#video-language-menu li.active').removeClass('active');
      $(this).parent('li').addClass('active');
    });
  }
});
