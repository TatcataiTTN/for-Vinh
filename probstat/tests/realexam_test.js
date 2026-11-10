// Kiểm thử trang đề thật: điền đáp số đúng/sai cho từng mã đề, chấm, làm lại. node realexam_test.js [URL]
const puppeteer=require('puppeteer-core');
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--no-sandbox']});
const p=await b.newPage();await p.setViewport({width:1100,height:900});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto(process.argv[2]||'http://localhost:18433/vi/de-thi-that-hk22/index.html',{waitUntil:'networkidle0'});
const D=await p.evaluate(()=>JSON.parse(document.getElementById('realexam-data').textContent));
console.log('mã đề',D.length,'katex-error',await p.$$eval('.katex-error',e=>e.length));
let bad=0;
for(let i=0;i<D.length;i++){
  await p.select('#realexam select',String(i));
  const d=D[i];
  for(let k=0;k<8;k++){await p.$eval('#rx'+k,(e,v)=>{e.value=v},String(d.ans[k]).replace('.',k%2?',':'.'))}
  const e=d.eans;const set=async(id,v)=>p.$eval('#'+id,(x,v)=>{x.value=v},String(v));
  await set('e_xb',e.xb);await set('e_s2',e.s2);await set('e_b0',e.b[0]);await set('e_b1',e.b[1]);await set('e_c0',e.c[0]);await set('e_c1',e.c[1]);
  await p.evaluate(()=>[...document.querySelectorAll('#realexam button')].find(x=>x.textContent==='Chấm bài').click());
  const t=await p.$eval('#rres',x=>x.textContent);
  if(!t.includes('10.0/10')){bad++;console.log('KHÔNG đủ điểm',d.code,t)}
  // làm lại rồi điền sai
  await p.evaluate(()=>[...document.querySelectorAll('#realexam button')].find(x=>x.textContent.startsWith('↺')).click());
  const empty=await p.$eval('#rx0',x=>x.value==='');if(!empty){bad++;console.log('reset lỗi',d.code)}
}
await p.select('#realexam select','0');
for(let k=0;k<8;k++)await p.$eval('#rx'+k,x=>{x.value='999'});
await p.evaluate(()=>[...document.querySelectorAll('#realexam button')].find(x=>x.textContent==='Chấm bài').click());
const t=await p.$eval('#rres',x=>x.textContent);console.log('sai hết ->',t);if(!t.includes('0.0/10'))bad++;
const ov=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2);console.log('tràn ngang:',ov,'| lỗi js:',errs,'| lỗi:',bad);
await p.screenshot({path:'/tmp/rx_top.png',clip:{x:0,y:0,width:1100,height:900}});
await b.close();process.exit(bad||errs.length?1:0)})();
