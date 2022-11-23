export default class HomePage {
  constructor(pageData) {
    const maps = new Maps();
    const centre = [-28.5, 25];
    const zoom = 5;
    maps.drawMapForHomepage('.home-map', centre, zoom);
  }
}
