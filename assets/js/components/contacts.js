import { logIfUnequal } from '../utils.js';

class OfficeContact {
  templateSelector = ".components .expand-block-with-list";

  constructor(office) {
    this.$element = $(this.templateSelector).clone();
    this.$itemTemplate = this.$element.find(".profile-info__item ").clone();
    this.$element.find(".profile-info__item ").remove();

    const $heading = this.$element.find(".expand-block__heading");
    $heading.text(office.role);
    const $innerHeading = this.$element.find(".profile-info__heading");
    $innerHeading.text(office.secretary.role);

    this.makeItem("fas fa-user-alt", office.name).insertBefore($innerHeading);
    this.makeItem("fas fa-phone", office.office_phone, "tel").insertBefore($innerHeading);
    this.makeItem("fas fa-envelope", office.email, "mailto").insertBefore($innerHeading);
    this.makeItem("fas fa-envelope", office.secretary.email, "mailto").insertAfter($innerHeading);
    this.makeItem("fas fa-phone", office.secretary.office_phone, "tel").insertAfter($innerHeading);
    this.makeItem("fas fa-user-alt", office.secretary.name).insertAfter($innerHeading);

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
  constructor(staff) {
    this.$element = $("#contacts");
    this.$contactContainer = this.$element.find(".expand-blocks");
    staff.officials.forEach((office) => {
      const contact = new OfficeContact(office);
      this.$contactContainer.append(contact.render());
    });
  }
}
