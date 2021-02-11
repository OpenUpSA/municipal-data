import {
  logIfUnequal,
  locale,
  formatDate,
  arrayJoin,
} from '../utils.js';
import { TextField, LinkedTextField } from './common.js';

function createMunicipalityLinks(municipalities) {
  return municipalities.map((municipality) => {
    const el = document.createElement("a");
    const id = `${municipality.full_geoid}-${municipality.slug}`;
    el.setAttribute("href", `/profiles/${id}`);
    el.setAttribute("class", "profile-notice__link");
    el.innerText = municipality.short_name;
    return el.outerHTML;
  }).join(', ');
}

function showProfileNotice(message) {
  const $notice = $(".profile-notice");
  const $text = $notice.find(".profile-notice__text");
  $text.html(message);
  $notice.removeClass("hidden");
}

export class ProfileHeader {
  constructor(
    geography,
    totalPopulation,
    populationDensity,
    demarcation,
  ) {
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

    // Handle disestablished municipality
    if (demarcation.disestablished) {
      const name = geography.name;
      const date = formatDate(new Date(demarcation.disestablished_date));
      const municipalities = demarcation.disestablished_to_geos;
      const links = createMunicipalityLinks(municipalities);
      showProfileNotice(`${name} was disestablished on ${date} and ` +
        `amalgamated into ${links}`);
    }
    // Handle municipality established after last audit or withing audit years
    if (demarcation.established_after_last_audit
      || demarcation.established_within_audit_years) {
      const name = geography.name;
      const date = formatDate(new Date(demarcation.established_date));
      const municipalities = demarcation.established_from_geos;
      const links = createMunicipalityLinks(municipalities);
      showProfileNotice(`${name} was established on ${date} ` +
        `through the amalgamation of ${links}`);
    }
    // Handle various municipal mergings
    if (demarcation.land_gained || demarcation.land_lost) {
      const messages = [];
      const name = geography.name;
      // Handle municipalities merged into the current one
      for (const data of demarcation.land_gained) {
        const date = formatDate(new Date(data.date));
        const municipalities = data.changes.map((change) => change.geo);
        const links = createMunicipalityLinks(municipalities);
        messages.push(`Part of ${links} became part of ${name} on ${date}`);
      }
      // Handle this municipality merging into another
      for (const data of demarcation.land_lost) {
        const date = formatDate(new Date(data.date));
        const municipalities = data.changes.map((change) => change.geo);
        const links = createMunicipalityLinks(municipalities);
        messages.push(`Part of ${name} became part of ${links} on ${date}`);
      }
      // Show the collective message (this won't look good, fix later)
      showProfileNotice(messages.join('<br />'));
    }

  }
}
