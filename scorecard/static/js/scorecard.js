$(document).ready(function(){

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

});
