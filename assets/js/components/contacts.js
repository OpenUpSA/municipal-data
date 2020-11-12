import { logIfUnequal } from '../utils.js';

class OfficeContact {
  templateSelector = ".components .expand-block-with-list";

  constructor(office) {
    this.$element = $(this.templateSelector).clone();
    this.$element.find(".expand-block__heading").text(office.role);
    this.$element.find(".profile-info__item:eq(0) > div:eq(1)").text(office.name);
    this.$element.find(".profile-info__heading").text(office.secretary.role);
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
