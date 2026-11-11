// Chụp ảnh các trang để xem bằng mắt: node tests/shots.js
const puppeteer=require('../../probstat/tests/node_modules/puppeteer-core');
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--no-sandbox']});
const p=await b.newPage();await p.setViewport({width:1100,height:900});const B='http://localhost:18434/';
await p.goto(B,{waitUntil:'networkidle0'});await p.screenshot({path:'/tmp/bt_home.png',fullPage:true});
await p.goto(B+'chuan-tac/',{waitUntil:'networkidle0'});
await p.$eval('[data-lk="a8"] input',e=>{e.value='7'});await p.click('[data-lk="a8"] .btn');
const el1=await p.$('#a8');await el1.scrollIntoView();await p.screenshot({path:'/tmp/bt_a8.png'});
await p.evaluate(()=>document.querySelector('#a7').scrollIntoView());await p.screenshot({path:'/tmp/bt_a7.png'});
await p.goto(B+'student/',{waitUntil:'networkidle0'});await p.evaluate(()=>document.querySelector('[data-lk="a9"]').scrollIntoView({block:'start'}));await p.screenshot({path:'/tmp/bt_a9.png'});
await p.goto(B+'luyen-tra/',{waitUntil:'networkidle0'});await p.$eval('.qbox input',e=>{e.value='1'});await p.click('.qbox .btn:not(.alt)');await p.screenshot({path:'/tmp/bt_luyen.png'});
await p.goto(B+'de-that/',{waitUntil:'networkidle0'});await p.evaluate(()=>{document.querySelector('details.tbd').open=true});await p.screenshot({path:'/tmp/bt_dethat.png',fullPage:true});
await b.close()})();
