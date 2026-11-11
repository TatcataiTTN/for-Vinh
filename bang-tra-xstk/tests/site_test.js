// Kiểm thử site Học tra bảng XSTK bằng Chrome thật: node tests/site_test.js [BASE]
const puppeteer=require('../../probstat/tests/node_modules/puppeteer-core');const fs=require('fs'),path=require('path');
const BASE=(process.argv[2]||'http://localhost:18434/').replace(/\/?$/,'/');
const V=JSON.parse(fs.readFileSync(path.join(__dirname,'vectors.json')));
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--no-sandbox']});
let fails=0;const log=(ok,m)=>{if(!ok){fails++;console.log('FAIL',m)}else console.log('ok  ',m)};
async function open(u,w){const p=await b.newPage();await p.setViewport({width:w||1100,height:900});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('response',r=>{if(r.status()>=400)errs.push('HTTP '+r.status()+' '+r.url())});await p.goto(BASE+u,{waitUntil:'networkidle0'});return [p,errs]}
const pages=['','chuan-tac/','student/','chi-binh-phuong/','luyen-tra/','de-that/','in-bang/'];
for(const u of pages){const [p,e]=await open(u);const ov=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2);log(!e.length&&!ov,'trang /'+u+' lỗi:'+JSON.stringify(e)+' tràn ngang:'+ov);await p.close()}
for(const u of ['','student/','chuan-tac/']){const [p]=await open(u,390);const ov=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2);log(!ov,'điện thoại 390px /'+u+' không tràn ngang');await p.close()}
{const [p]=await open('chuan-tac/');let bad=0;
 const r=await p.evaluate((V)=>{const o=[];V.phi.forEach(a=>o.push(Math.abs(PS.Phi(a[0])-a[1])));V.z.forEach(a=>o.push(Math.abs(PS.zq(a[0])-a[1])));return o},V);r.forEach(x=>{if(x>1e-7)bad++});
 const rt=await p.evaluate((V)=>V.t.map(a=>Math.abs(PS.tq(a[1],a[0])-a[2])/Math.max(1,Math.abs(a[2]))),V);rt.forEach(x=>{if(x>1e-6)bad++});
 const rc=await p.evaluate((V)=>V.chi.map(a=>Math.abs(PS.chiq(a[1],a[0])-a[2])/Math.max(1,a[2])),V);rc.forEach(x=>{if(x>1e-6)bad++});
 log(bad===0,'hàm Φ, t, χ² của JS khớp SciPy ('+(r.length+rt.length+rc.length)+' vector, lệch '+bad+')');
 const n7=await p.$$eval('#tbl-a7 td[data-k]',e=>e.length);log(n7===300,'A7 có 300 ô Φ ('+n7+')');
 const c=await p.$eval('#tbl-a7 td[data-k="1.23"]',e=>e.textContent);log(c==='8907','A7 ô 1.23 = '+c);
 const a8=await p.$eval('#tbl-a8 td[data-p="93"][data-c="0"]',e=>e.textContent);log(a8==='1.476','A8 hàng 93 = '+a8);
 const a8n=await p.$eval('#tbl-a8 td[data-p="7"][data-c="0"]',e=>e.textContent);log(a8n==='−1.476','A8 hàng 7 = '+a8n);
 const ans=async(sel)=>p.$eval(sel,e=>e.textContent);
 async function set(sel,v){await p.$eval(sel,(e,v)=>{e.value=v},v)}
 const w7='[data-lk="a7"]';await set(w7+' input','1.2308');await p.click(w7+' .btn');let t=await ans(w7+' .ans');log(t.includes('0.8907'),'widget A7 z=1.2308 → '+t);
 await set(w7+' input','-0.57');await p.click(w7+' .btn');t=await ans(w7+' .ans');log(t.includes('0.2843'),'widget A7 z=−0.57 → '+t);
 const hl=await p.$eval('#tbl-a7 .hl',e=>e.textContent);log(hl==='7157','ô tô sáng của z=0.57 = '+hl);
 const w8='[data-lk="a8"]';await set(w8+' input','7');await p.click(w8+' .btn');t=await ans(w8+' .ans');log(t.includes('1.476'),'widget A8 α=7% → '+t);
 const h8=await p.$eval('#tbl-a8 .hl',e=>e.textContent);log(h8==='1.476','A8 tô sáng: '+h8);
 await p.select(w8+' select','D');await set(w8+' input','90');await p.click(w8+' .btn');t=await ans(w8+' .ans');log(t.includes('1.645'),'widget A8 D=90% → '+t);
 await p.select(w8+' select','alpha');await set(w8+' input','1.5');await p.click(w8+' .btn');t=await ans(w8+' .ans');log(/2\.19|2\.18/.test(t),'widget A8 α=1.5% (nội suy) → '+t);
 await p.close()}
{const [p]=await open('student/');const ans=async s=>p.$eval(s,e=>e.textContent);const w='[data-lk="a9"]';
 const run=async(mode,df,v)=>{await p.select(w+' select',mode);await p.$eval(w+' label:nth-of-type(2) input',(e,x)=>{e.value=x},df);await p.$eval(w+' label:nth-of-type(3) input',(e,x)=>{e.value=x},v);await p.click(w+' .btn');return ans(w+' .ans')};
 let t=await run('F','9','0.95');log(t.includes('1.83'),'A9 (9; 0.95) → '+t);
 t=await run('gamma','15','95');log(t.includes('2.13'),'A9 γ=95%, m=15 → '+t);
 t=await run('alpha','18','7');log(t.includes('1.570')&&t.includes('1.544'),'A9 α=7%, m=18 (nội suy) → '+t);
 t=await run('gamma','31','90');log(t.includes('1.698')&&t.includes('1.696'),'A9 γ=90%, m=31 (nội suy) → '+t);
 t=await run('F','inf','0.95');log(t.includes('1.65'),'A9 (∞; 0.95) → '+t);
 await p.close();
 const w10='[data-lk="a10"]';const [q]=await open('chi-binh-phuong/');
 await q.$eval(w10+' label:nth-of-type(1) input',e=>{e.value='3'});await q.$eval(w10+' label:nth-of-type(2) input',e=>{e.value='0.99'});await q.click(w10+' .btn');t=await q.$eval(w10+' .ans',e=>e.textContent);log(t.includes('11.34'),'A10 (3; 0.99) → '+t);
 await q.$eval(w10+' label:nth-of-type(1) input',e=>{e.value='150'});await q.$eval(w10+' label:nth-of-type(2) input',e=>{e.value='0.95'});await q.click(w10+' .btn');t=await q.$eval(w10+' .ans',e=>e.textContent);log(/179\./.test(t),'A10 m=150 xấp xỉ → '+t);await q.close()}
{const [p,e]=await open('luyen-tra/');const QS=await p.evaluate(()=>window.QUESTIONS);let bad=0,done=0;
 for(let i=0;i<QS.length+5;i++){const txt=await p.$eval('.qtxt',x=>x.textContent).catch(()=>null);if(!txt)break;const id=+/Câu (\d+)\./.exec(txt)[1];const q=QS.find(x=>x.id===id);
  await p.$eval('.qbox input',(x,v)=>{x.value=v},String(q.a));await p.click('.qbox .btn:not(.alt)');const fb=await p.$eval('.fb',x=>x.textContent);if(!fb.includes('Đúng')){bad++;if(bad<4)console.log('  sai',q.q,q.a,fb.slice(0,80))}done++;await p.click('.fb .btn')}
 log(bad===0&&done===QS.length,'làm đúng '+done+'/'+QS.length+' câu luyện (lỗi '+bad+')');
 const sc=await p.$eval('.quiz-score',x=>x.textContent);log(sc.includes('đúng '+QS.length),'tiến độ: '+sc);
 await p.evaluate(()=>[...document.querySelectorAll('.row button')].find(x=>x.textContent.includes('Làm lại')).click());
 await p.$eval('.qbox input',x=>{x.value='99999'});await p.click('.qbox .btn:not(.alt)');const fb=await p.$eval('.fb',x=>x.textContent);log(fb.includes('Sai'),'đáp số sai bị chấm sai');
 const hl=await p.$$eval('.hl',x=>x.length);log(hl>=1,'ô đúng được tô sáng sau khi kiểm tra ('+hl+')');log(!e.length,'luyện tập không lỗi JS: '+JSON.stringify(e));await p.close()}
{const [p]=await open('in-bang/');const n=await p.$$eval('table.tb',x=>x.length);log(n===4,'trang in có 4 bảng');await p.close()}
{const [p]=await open('de-that/');const n=await p.$$eval('details.tbd',x=>x.length);log(n===10,'trang đề thật có 10 mã đề');await p.close()}
console.log(fails?('TỔNG: '+fails+' lỗi'):'TỔNG: tất cả kiểm thử đạt');await b.close();process.exit(fails?1:0)})();
