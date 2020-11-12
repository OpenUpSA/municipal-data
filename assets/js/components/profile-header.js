import { logIfUnequal, locale, capFirst } from '../utils.js';
import { TextField, LinkedTextField } from './common.js';

export class ProfileHeader {
  constructor(geography, totalPopulation, populationDensity) {
    new TextField(".page-heading__title", geography.short_name);
    new TextField(".profile-metric__population", locale.format(",")(totalPopulation));
    new TextField(".profile-metric__size", locale.format(",.1f")(geography.square_kms));
    new TextField(".profile-metric__density", locale.format(",.1f")(populationDensity));

    if (geography.category_name === "metro municipality") {
      const $container = $(".page-heading__metro");
      $container.removeClass("hidden");
      new TextField($container.find(".page-heading__geo-parent-3"), geography.province_name);
    } else if (geography.category_name === "local municipality") {
      const $container = $(".page-heading__local-muni");
      $container.removeClass("hidden");
      new LinkedTextField(
        $container.find(".page-heading__geo-parent-1"),
        geography.ancestors[0].short_name,
        `/profiles/${ geography.ancestors[0].full_geoid }-${ geography.ancestors[0].slug }`
      );
      new TextField($container.find(".page-heading__geo-parent-3"), geography.province_name);
    } else if (geography.category_name === "district municipality") {
      const $container = $(".page-heading__district-muni");
      $container.removeClass("hidden");
      new TextField($container.find(".page-heading__geo-parent-3"), geography.province_name);
    }


  }
}
