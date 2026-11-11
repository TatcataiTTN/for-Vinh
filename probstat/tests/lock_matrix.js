// Ma trận khóa đáp án: mỗi trang chỉ mở bằng ĐÚNG mật khẩu của nó. Mật khẩu truyền qua biến môi trường (không ghi vào file):
//   P1=<mật khẩu trang lần 1> P2=<mật khẩu trang lần 2> POLD=<mật khẩu cũ của trang 1> node tests/lock_matrix.js [BASE]
const puppeteer=require('puppeteer-core');
const BASE=(process.argv[2]||'http://localhost:18433/vi/').replace(/\/?$/,'/');
const PAGES=[{u:'de-giua-ky/index.html',marker:['53856','1260','0,5888'],ok:process.env.P1},{u:'de-giua-ky-2/index.html',marker:['30240','0,6818','0,9201'],ok:process.env.P2}];
const TRY=[['P1',process.env.P1],['P2',process.env.P2],['POLD',process.env.POLD],['rỗng',''],['sai','khong-phai-mat-khau']];
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--no-sandbox']});let fails=0;
for(const pg of PAGES){for(const [name,pw] of TRY){const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));await p.goto(BASE+pg.u,{waitUntil:'networkidle0'});
 const before=await p.evaluate(m=>m.some(x=>document.body.innerText.includes(x)),pg.marker);
 await p.$eval('#pw',(e,v)=>{e.value=v},pw||'');await p.click('#unlock');await new Promise(r=>setTimeout(r,3000));
 const opened=await p.evaluate(m=>m.every(x=>document.body.innerText.includes(x)),pg.marker);const msg=await p.$eval('#lockmsg',e=>e.textContent).catch(()=>'');
 const expect=pw===pg.ok&&pw!=='';const good=!before&&opened===expect&&errs.length===0;if(!good)fails++;
 console.log((good?'ok  ':'FAIL')+' '+pg.u.split('/')[0]+' · mật khẩu '+name+' → '+(opened?'MỞ':'khóa')+(expect?' (đúng kỳ vọng: mở)':' (đúng kỳ vọng: khóa)')+(good?'':' | trước khi nhập lộ: '+before+' msg='+msg+' lỗi '+errs));await p.close()}}
console.log(fails?('TỔNG: '+fails+' lỗi'):'TỔNG: ma trận mật khẩu đạt');await b.close();process.exit(fails?1:0)})();
