const puppeteer = require('puppeteer');

async function printPDF(url) {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--disable-dev-shm-usage', '--no-sandbox'],
  });
  try {
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });
    // networkidle2 allows the mapit boundary requests to still be in flight, and
    // the map only gets a view (and loads tiles) once those have been drawn.
    // Print without the map rather than fail if mapit is slow or down.
    if (await page.$('.leaflet-container')) {
      await page.waitForFunction(
        () => document.querySelectorAll('.leaflet-overlay-pane path').length > 1
          && !document.querySelector('.leaflet-tile:not(.leaflet-tile-loaded)'),
        { timeout: 30000 },
      ).catch((err) => console.error(`Map not ready, printing without it: ${err.message}`));
    }
    const pdf = await page.pdf({ format: 'A4' });
    return pdf;
  } finally {
    await browser.close();
  }
}

const url = process.argv[2];

printPDF(url).then((buffer) => process.stdout.write(buffer)).catch((err) => {
  console.error(err);
  process.exit(1);
});
