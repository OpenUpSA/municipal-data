function logIfUnequal(a, b) {
  if (a !== b) {
    console.error(`${a} !== ${b}`);
  }
}

class Title {
  selector = ".page-heading__title";

  constructor(title) {
    this.element = $(this.selector);
    logIfUnequal(1, this.element.length);
    this.element.text(title);
  }
}

class TextField {
  constructor(selector, value) {
    this.element = $(selector);
    logIfUnequal(1, this.element.length);
    this.element.text(value);
  }
}
const pageData = JSON.parse(document.getElementById('page-data').textContent);

new Title(pageData.geography.short_name);
new TextField(".profile-metric__population", pageData.total_population);
