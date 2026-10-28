// Kiểm thử khóa đáp án: node lock_test.js [URL]
const puppeteer=require('puppeteer-core');
const URL=process.argv[2]||'http://localhost:18433/vi/de-giua-ky/index.html';
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--no-sandbox']});
const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));await p.goto(URL,{waitUntil:'networkidle0'});
const txt=()=>p.evaluate(()=>document.body.innerText);
let t=await txt();console.log('trước:',t.includes('53856'), (await p.$$('.locked')).length,'khối khóa');
await p.type('#pw','sai');await p.click('#unlock');await new Promise(r=>setTimeout(r,2500));
console.log('sai mk ->',await p.$eval('#lockmsg',e=>e.textContent),'| lộ:',(await txt()).includes('53856'));
await p.$eval('#pw',e=>e.value='');await p.type('#pw',process.env.PW);await p.click('#unlock');await new Promise(r=>setTimeout(r,3000));
t=await txt();console.log('đúng mk -> lộ 53856:',t.includes('53856'),'| 1260:',t.includes('1260'),'| 0,5888:',t.includes('0,5888'),'| lỗi:',errs);
await b.close()})();
