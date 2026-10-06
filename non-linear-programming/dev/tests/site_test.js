// Kiểm thử trình duyệt thật (puppeteer-core + Chrome hệ thống). Dùng: node site_test.js <baseUrl> <modulePath...>
const puppeteer = require('/opt/homebrew/lib/node_modules/@mermaid-js/mermaid-cli/node_modules/puppeteer-core');
(async () => {
  const base = process.argv[2]; const paths = process.argv.slice(3);
  const browser = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new' });
  let fails = 0;
  for (const p of paths) {
    const page = await browser.newPage(); await page.setViewport({ width: 1280, height: 900 });
    const errs = [];
    page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    page.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
    page.on('requestfailed', r => errs.push('REQFAIL ' + r.url()));
    const resp = await page.goto(base + p, { waitUntil: 'networkidle0', timeout: 60000 });
    console.log('==', p, resp.status());
    const info = await page.evaluate(() => {
      const slides = document.querySelectorAll('.mdeck-slide').length;
      const kerr = document.querySelectorAll('.katex-error').length;
      const kok = document.querySelectorAll('.katex').length;
      const q = document.querySelectorAll('.quiz .qitem').length;
      const rawTeX = (document.body.innerText.match(/\\\(|\\\[/g) || []).length;
      const widgets = [...document.querySelectorAll('.widget')].map(w => w.getAttribute('data-widget') + ':' + (w.querySelector('canvas') ? 'canvas' : 'nocanvas') + ':' + w.innerText.length);
      const imgs = [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src);
      return { slides, kerr, kok, q, rawTeX, widgets, brokenImgs: imgs.length };
    });
    console.log(JSON.stringify(info));
    // duyệt qua tất cả slide: đo tràn (scrollHeight > clientHeight) & katex lỗi
    const overflow = await page.evaluate(async () => {
      const deck = document.querySelector('.mdeck'); if (!deck) return [];
      const n = deck.querySelectorAll('.mdeck-slide').length; const bad = [];
      for (let i = 0; i < n; i++) {
        deck._go(i); await new Promise(r => setTimeout(r, 120));
        const s = deck.querySelectorAll('.mdeck-slide')[i];
        const fs = parseFloat(s.style.fontSize);
        if (s.scrollHeight > s.clientHeight + 2) bad.push((i + 1) + ':' + s.getAttribute('data-title') + ' fs=' + fs.toFixed(1));
      }
      deck._go(0); return bad;
    });
    console.log('slide tràn:', overflow.length ? overflow.join(' | ') : 'không');
    // quiz: bấm đáp án đầu của câu MCQ đầu, kiểm tra giải thích hiện + reset
    const qres = await page.evaluate(async () => {
      const first = document.querySelector('.quiz .qitem .opt'); if (!first) return 'no quiz';
      first.click(); await new Promise(r => setTimeout(r, 100));
      const item = first.closest('.qitem');
      const shown = item.querySelector('.explain').classList.contains('show');
      const marked = item.querySelectorAll('.opt.correct').length === 1;
      item.querySelector('.retry').click(); await new Promise(r => setTimeout(r, 100));
      const again = document.querySelector('.quiz .qitem .opt:not([data-done])') !== null;
      return { explainShown: shown, correctMarked: marked, retryWorks: again };
    });
    console.log('quiz:', JSON.stringify(qres));
    if (errs.length) { console.log('LỖI:', errs.slice(0, 8)); fails += errs.length; }
    if (info.kerr) fails++;
    await page.close();
  }
  await browser.close(); console.log('FAILS', fails); process.exit(fails ? 1 : 0);
})();
