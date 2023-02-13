import { logIfUnequal } from '../utils.js';

class OfficeContact {
  templateSelector = ".components .expand-block-with-list";

  constructor(office) {
    this.$element = $(this.templateSelector).clone();
    this.$itemTemplate = this.$element.find(".profile-info__item ").clone();
    this.$element.find(".profile-info__item ").remove();

    const $heading = this.$element.find(".expand-block__trigger_heading");
    $heading.text(office.role);
    const $innerHeading = this.$element.find(".profile-info__heading");
    $innerHeading.text(office.secretary.role);

    this.makeItem("fas fa-user-alt", `${office.title} ${office.name}`).insertBefore($innerHeading);
    this.makeItem("fas fa-phone", office.office_phone, "tel").insertBefore($innerHeading);
    this.makeItem("fas fa-envelope", office.email, "mailto").insertBefore($innerHeading);
    this.makeItem("fas fa-envelope", office.secretary.email, "mailto").insertAfter($innerHeading);
    this.makeItem("fas fa-phone", office.secretary.office_phone, "tel").insertAfter($innerHeading);
    this.makeItem(
      "fas fa-user-alt",
      `${office.secretary.title} ${office.secretary.name}`
    ).insertAfter($innerHeading);

    this.$staffExpand = this.$element.find(".expand-block__trigger");
    this.$staffExpand.on('click', ((e) => {
      gtag('event', 'contact_info', {
        category: "Contacts",
        action: "Expand",
        label: `${office.role}`,
      });
    }));
  }

  makeItem(iconClasses, value, linkType) {
    const $item = this.$itemTemplate.clone();
    $item.find(".profile-item__item_icon > div").attr("class", iconClasses);
    if (linkType) {
      const anchor = $("<a></a>").attr("href", `${linkType}:${value}`);
      anchor.text(value);
      $item.find(".profile-item__item-value").html(anchor);
    } else {
      $item.find(".profile-item__item-value").text(value);
    }
    return $item;
  }

  render() {
    return this.$element;
  }
}

export class ContactSection {
  constructor(muniContact, staff, geography) {
    this.$element = $("#contacts");

    this.$element.find(".date-updated").text(`Last updated  ${staff.updated_date}`);

    this.$contactContainer = this.$element.find(".expand-blocks");
    staff.officials.forEach((office) => {
      const contact = new OfficeContact(office);
      this.$contactContainer.append(contact.render());
    });

    const officials = staff.officials;
    const emails = [];
    if (officials[0].email) emails.push(officials[0].email);
    if (officials[0].secretary.email) emails.push(officials[0].secretary.email);
    if (officials[1].email) emails.push(officials[1].email);
    if (officials[1].secretary.email) emails.push(officials[1].secretary.email);
    if (officials[2].email) emails.push(officials[2].email);
    if (officials[2].secretary.email) emails.push(officials[2].secretary.email);
    if (emails.length >= 2) {
      const body = `You can explore Municipal Finance for ${geography.name}  at ${window.location}`;
      const url = ('mailto:' +
        emails.slice(0, 2).join(';') +
        '?cc=feedback@municipalmoney.gov.za' +
        '&subject=' + encodeURIComponent('Feedback via Municipal Money') +
        '&body=\n\n\n' + encodeURIComponent(body));
      this.$element.find(".button--email-muni")
        .attr("href", url)
        .css("display", "grid");
    }

    if (muniContact.phone_number) {
      this.$element.find(".button--phone-muni")
        .attr("href", `tel:${muniContact.phone_number}`)
        .css("display", "grid")
        .find("div:eq(2)")
        .text(muniContact.phone_number);
    }

    if (muniContact.url) {
      this.$element.find(".button--muni-site")
        .attr("href", muniContact.url)
        .css("display", "grid")
        .find("div:eq(2)")
        .text(muniContact.url);
    }

    let address = "";
    [
      muniContact.street_address_1,
      muniContact.street_address_2,
      muniContact.street_address_3,
      muniContact.street_address_4,
    ].forEach((line) => { if (line) address += `${line}\n`; });
    if (address) {
      const addressBlock = this.$element.find(".muni-address");
      addressBlock.css("display", "block");
      addressBlock.find(".button__icon")
        .css("display", "inline")
        .css("height", "auto");
      addressBlock.find("div:eq(2)")
        .text(address)
        .css("white-space", "pre-wrap")
        .css("display", "inline");
    }

    this.$staffLinks = this.$contactContainer.find(".expand-block__trigger a");
    this.$muniLinks = this.$element.find("a");
    this.$staffLinks.on('click', ((e) => {
      gtag('event', 'contact_info', {
        category: "Contacts",
        action: "Click",
        label: `${$(e.target).text()}`,
      });
    }));
    this.$muniLinks.on('click', ((e) => {
      gtag('event', 'contact_info', {
        category: "Contacts",
        action: "Click",
        label: "Municipal wide contacts",
      });
    }));
  }
}
