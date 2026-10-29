const puppeteer = require('puppeteer');

async function printPDF(url) {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--disable-dev-shm-usage', '--no-sandbox'],
  });
  try {
    const page = await browser.newPage();
    const response = await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });
    // Don't print error pages - fail so the caller doesn't serve them as a PDF
    if (!response || !response.ok()) {
      throw new Error(`Failed to load ${url}: HTTP ${response ? response.status() : 'no response'}`);
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
