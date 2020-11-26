import ProfilePage from './pages/profile.js';
import HomePage from './pages/home.js';

$(function() {
  const pageType = $("body").data("page");
  switch (pageType) {
  case "home":
    new HomePage();
    break;
  case "municipality-profile":
    new ProfilePage();
    break;
  case "terms":
    break;
  case "help":
    break;
  default:
    console.error("No class for page type: ", pageType);
  }
});
