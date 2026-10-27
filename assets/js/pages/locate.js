const LOOKUP_TIMEOUT_MS = 10000;

export default class LocatePage {
  constructor(pageData) {
    this.$spinner = $('.location-block--search');

    if (pageData.nope === true) {
      this.noLocation();
      return;
    }

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        this.foundLocation.bind(this),
        this.noLocation.bind(this),
        { timeout: 10000, maximumAge: 300000 },
      );
    } else {
      alert('Location search not supported by your browser. Please try another browser or device.');
    }
  }

  foundLocation(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    // Give up on the lookup rather than leave the reader on a spinner
    setTimeout(() => {
      window.stop();
      this.noLocation();
    }, LOOKUP_TIMEOUT_MS);
    window.location = `/locate/?lat=${lat}&lon=${lon}`;
  }

  noLocation() {
    this.$spinner.hide();
    $('.location-block--not-found').show();
  }
}
