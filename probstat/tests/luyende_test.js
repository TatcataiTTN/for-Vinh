// Kiểm thử Luyện đề + Kho đề: node luyende_test.js [BASE]
const puppeteer=require('puppeteer-core');
const BASE=(process.argv[2]||'http://localhost:18433/vi/').replace(/\/?$/,'/');
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--no-sandbox']});
const p=await b.newPage();await p.setViewport({width:1100,height:900});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('response',r=>{if(r.status()>=400)errs.push('HTTP '+r.status()+' '+r.url())});
let bad=0;
await p.goto(BASE+'luyen-de/index.html',{waitUntil:'networkidle0'});
const tabs=await p.$$eval('#exam .row button',e=>e.length);console.log('số đề',tabs);if(tabs!==12)bad++;
await p.evaluate(()=>[...document.querySelectorAll('#exam .row button')].find(x=>x.textContent==='Đề 9').click());
const hk=await p.$$eval('#exam .qitem',els=>els.filter(e=>e.textContent.includes('HK2.2')).length);console.log('câu từ đề thật HK2.2 trong đề 9:',hk);if(hk<6)bad++;
await p.$$eval('#exam .qitem',els=>els.forEach(e=>e.querySelector('.opt').click()));
await p.evaluate(()=>[...document.querySelectorAll('#exam button')].find(x=>x.textContent==='Nộp bài').click());
const r=await p.$eval('#res',x=>x.textContent);console.log(r);if(!/Kết quả: \d+\/15/.test(r))bad++;
await p.goto(BASE+'kho-de/index.html',{waitUntil:'networkidle0'});
const links=await p.$$eval('main a',a=>a.map(x=>x.href));let dead=0;
for(const u of [...new Set(links)].filter(u=>u.startsWith('http://localhost')&&!u.includes('#'))){const rr=await p.goto(u,{waitUntil:'domcontentloaded'});if(rr.status()>=400){dead++;console.log('chết',u)}}
console.log('liên kết kho đề kiểm:',links.length,'chết:',dead);if(dead)bad++;
console.log('lỗi js/http:',errs,'| lỗi:',bad);await b.close();process.exit(bad||errs.length?1:0)})();
