/* Helper routines for managing the head-to-head comparison view.
 *
 * They ensure that the two iframes are sized to match the height
 * of their content, to prevent scrolling.
 */
function Head2Head() {
  var self = this;

  self.initParent = function() {
    // this is the parent frame in the head-to-head view
    self.isParent = true;
    self.isChild = false;
  };

  self.initChild = function() {
    // this is a child frame in the head-to-head view
    self.isParent = false;
    self.isChild = true;

    $('body').addClass('profile-head2head-frame');
    $('body').on('click', 'a[href]', self.navigateTo);

    // set the frame height
    setTimeout(self.resizeChild, 500);
    $(window).on('resize', _.debounce(self.resizeChild, 500));
  };

  self.resizeChild = function(e) {
    // set the iframe to fit the size of the child
    var height = document.body.offsetHeight + 50,
        frame = $(window.frameElement);

    if (frame.height() != height) {
      // height changed, update the iframe and check again in a few msecs
      frame.height(height);
      setTimeout(self.resizeChild, 500);
    }
  };

  self.navigateTo = function(e) {
    // open links in the parent window
    if (e.target.href && e.target.href.indexOf('#') == -1 && e.target.getAttribute('target') != "_blank") {
      e.preventDefault();
      window.parent.location = e.target.href;
    }
  };
}

var h2h = new Head2Head();

if (window.parent != window && window.parent.location.pathname.indexOf('/compare/') > -1) {
  h2h.initChild();
} else if (window.location.pathname.indexOf('/compare/') > -1) {
  h2h.initParent();
}
