import ProfilePage from './pages/profile.js';
import HomePage from './pages/home.js';
import LocatePage from './pages/locate.js';
import HelpPage from './pages/help.js';
import './polyfills/custom-event';

$(function() {
  const pageType = $("body").data("page");
  const pageJSON = document.getElementById('page-data').textContent;
  const pageData = pageJSON ? JSON.parse(pageJSON) : null;

  switch (pageType) {
  case "home":
    new HomePage(pageData);
    break;
  case "municipality-profile":
    new ProfilePage(pageData);
    break;
  case "locate":
    new LocatePage(pageData);
    break;
  case "terms":
    break;
  case "help":
    new HelpPage();
    break;
  default:
    console.error("No class for page type: ", pageType);
  }
});

$("#Municipality-Search-Hero, #municipality-search-2").keypress(function(e){
  if(e.keyCode === 13){
    e.preventDefault();
  }
});

window.testSentry = () => nonExistentFunction("Something");