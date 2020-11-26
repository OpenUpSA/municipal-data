export default class HomePage {
  constructor(pageData) {
    const maps = new Maps();
    var centre = [-28.5, 25];
    var zoom = 5;
    maps.drawMapForHomepage(".home-map", centre, zoom);
  }
}
