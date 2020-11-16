const puppeteer = require('puppeteer');

async function printPDF(url) {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--disable-dev-shm-usage', '--no-sandbox']
  });
  const page = await browser.newPage();
  await page.goto(url, {waitUntil: 'networkidle0'});
  const pdf = await page.pdf({ format: 'A4' });

  await browser.close();
  return pdf;
};

const url = process.argv[2];

printPDF(url).then((buffer) => process.stdout.write(buffer));
