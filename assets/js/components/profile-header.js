import { logIfUnequal, locale } from '../utils.js';
import { TextField, LinkedTextField } from './common.js';

export class ProfileHeader {
  constructor(geography, totalPopulation, populationDensity) {
    new TextField(".page-heading__title", geography.short_name);
    new TextField(".profile-metric__population", locale.format(",")(totalPopulation));
    new TextField(".profile-metric__size", locale.format(",.1f")(geography.square_kms));
    new TextField(".profile-metric__density", locale.format(",.1f")(populationDensity));

    if (geography.category_name === "metro municipality") {
      const $container = $(".page-heading__muni-info--metro");
      $container.css("display", "unset");
      $container.find(".page-heading__muni-type").text("Metro municipality");
      new TextField($container.find(".page-heading__geo-parent-3"), geography.province_name);
    } else if (geography.category_name === "local municipality") {
      const $container = $(".page-heading__muni-info--local");
      $container.css("display", "unset");
      new LinkedTextField(
        $container.find(".page-heading__geo-parent-1"),
        geography.ancestors[0].short_name,
        `/profiles/${ geography.ancestors[0].full_geoid }-${ geography.ancestors[0].slug }`
      );
      new TextField($container.find(".page-heading__geo-parent-3"), geography.province_name);
    } else if (geography.category_name === "district municipality") {
      const $container = $(".page-heading__muni-info--district");
      $container.css("display", "unset");
      new TextField($container.find(".page-heading__geo-parent-3"), geography.province_name);
    }


  }
}
