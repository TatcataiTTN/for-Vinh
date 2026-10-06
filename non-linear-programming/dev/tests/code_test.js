// Kiểm thử trang 'Thực hành code' trong Chrome thật (cần mạng để tải Pyodide). Dùng: node code_test.js <baseUrl>
// Đòi hỏi: lời giải mẫu của TỪNG bài đạt mọi test; ca SAI KẾT QUẢ, LỖI CHẠY, SyntaxError, QUÁ GIỜ nhận diện đúng; chạy lại sau TLE; đầu vào riêng; lưu tiến độ.
const puppeteer = require('/opt/homebrew/lib/node_modules/@mermaid-js/mermaid-cli/node_modules/puppeteer-core');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const base = process.argv[2];
  const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new' });
  const pg = await b.newPage(); await pg.setViewport({ width: 1280, height: 1600 });
  const errs = []; pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error' && !/favicon/.test(m.text())) errs.push(m.text()); });
  let bad = 0; const log = (ok, m) => { console.log((ok ? 'ok   ' : 'FAIL ') + m); if (!ok) bad++; };
  await pg.goto(base + 'code/index.html', { waitUntil: 'networkidle0' });
  await pg.waitForSelector('.code-card');
  const ex = await pg.evaluate(() => JSON.parse(document.getElementById('code-data').textContent));
  log(ex.length === 7, 'số bài web: ' + ex.length);
  async function submit(id, code, btn, wait) {
    await pg.evaluate(id => { const r = document.querySelector('#bai-' + id + ' .res'); r.style.display = 'none'; r.innerHTML = ''; }, id);
    await pg.evaluate((id, code) => { const ta = document.querySelector('#bai-' + id + ' .code-ta'); ta.value = code; ta.dispatchEvent(new Event('input')); }, id, code);
    await pg.evaluate((id, btn) => document.querySelector('#bai-' + id + ' ' + btn).click(), id, btn);
    for (let i = 0; i < (wait || 240); i++) { await sleep(500); const t = await pg.$eval('#bai-' + id + ' .res', e => e.style.display === 'none' ? '' : e.innerText); if (t) return t; }
    return '(hết giờ chờ)';
  }
  for (const e of ex) {
    const t = await submit(e.id, e.reference, '.b-all');
    const m = t.match(/(\d+)\/(\d+) test đạt/);
    log(m && m[1] === m[2] && +m[2] === e.tests.length, e.id + ' lời giải mẫu: ' + (m ? m[0] : t.slice(0, 120)));
  }
  const id = 'classify';
  let t = await submit(id, 'def classify_matrix(A, tol=1e-9):\n    return "PD"', '.b-all'); log(/SAI KẾT QUẢ/.test(t), 'SAI KẾT QUẢ nhận diện');
  t = await submit(id, 'def classify_matrix(A, tol=1e-9):\n    return 1/0', '.b-all'); log(/LỖI CHẠY/.test(t) && /ZeroDivisionError/.test(t), 'LỖI CHẠY + tên lỗi');
  t = await submit(id, 'def classify_matrix(A:', '.b-all'); log(/LỖI CHẠY/.test(t) && /SyntaxError/.test(t), 'SyntaxError hiển thị');
  t = await submit(id, 'x = 1', '.b-all'); log(/Chưa định nghĩa hàm classify_matrix/.test(t), 'thiếu hàm được báo rõ');
  t = await submit(id, 'def classify_matrix(A, tol=1e-9):\n    while True: pass', '.b-vis', 120); log(/QUÁ GIỜ/.test(t), 'QUÁ GIỜ (TLE) nhận diện');
  const ref = ex.find(x => x.id === id).reference;
  t = await submit(id, ref, '.b-all'); log(/(\d+)\/\1 test đạt/.test(t), 'chạy lại sau TLE (worker khởi động lại)');
  // đầu vào riêng
  await pg.evaluate(id => { document.querySelector('#bai-' + id + ' .b-custom').click(); const ci = document.querySelector('#bai-' + id + ' .custom-in'); ci.value = '[[[2,1],[1,2]]]'; const r = document.querySelector('#bai-' + id + ' .res'); r.style.display = 'none'; r.innerHTML = ''; document.querySelector('#bai-' + id + ' .b-crun').click(); }, id);
  let custom = ''; for (let i = 0; i < 60; i++) { await sleep(500); custom = await pg.$eval('#bai-' + id + ' .res', e => e.innerText); if (/PD/.test(custom)) break; }
  log(/"PD"/.test(custom), 'đầu vào riêng cho kết quả PD: ' + custom.slice(0, 40));
  const passed = await pg.evaluate(() => Object.keys(localStorage).filter(k => /nlp-code-v1-.*-pass/.test(k) && localStorage.getItem(k) === '1').length);
  log(passed === 7, 'đã lưu tiến độ ' + passed + '/7 bài');
  log(errs.length === 0, 'không lỗi JS ' + JSON.stringify(errs.slice(0, 3)));
  console.log(bad ? 'CÓ ' + bad + ' LỖI' : 'TỔNG: tất cả kiểm thử đạt'); await b.close(); process.exit(bad ? 1 : 0);
})();
