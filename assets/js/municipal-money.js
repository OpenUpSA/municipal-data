function logIfUnequal(a, b) {
  if (a !== b) {
    console.error(`${a} !== ${b}`);
  }
}

class Title {
  getSelector = () => ".page-heading__title";

  constructor(title) {
    this.element = $(this.getSelector());
    logIfUnequal(1, this.element.length);
    this.element.text(title);
  }
}

const pageData = JSON.parse(document.getElementById('page-data').textContent);

new Title(pageData.geography.name);
