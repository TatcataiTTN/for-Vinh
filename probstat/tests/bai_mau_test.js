const puppeteer=require('puppeteer-core');
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--no-sandbox']});
const p=await b.newPage();await p.setViewport({width:1280,height:900});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto(process.argv[2]||'http://localhost:18433/vi/bai-mau-tu-luan/index.html',{waitUntil:'networkidle0'});
const n=await p.$$eval('.mdeck-slide',e=>e.length);const ke=await p.$$eval('.katex-error',e=>e.length);
console.log('slide',n,'katex-error',ke,'lỗi js',errs);
const want=new Set((process.argv[3]||'').split(',').filter(Boolean).map(Number));
for(let i=0;i<n;i++){const h=await p.evaluate(()=>{const s=document.querySelector('.mdeck-slide.active, .mdeck-slide.on, .mdeck-slide.current')||[...document.querySelectorAll('.mdeck-slide')].find(x=>x.offsetParent);return s?[s.scrollHeight,s.clientHeight]:null});
 if(h&&h[0]>h[1]+2)console.log('slide',i+1,'cuộn dọc',h);
 if(want.has(i+1)){const el=await p.$('.mdeck');await el.screenshot({path:`/tmp/bm_${i+1}.png`})}
 await p.click('.mdeck-next');await new Promise(r=>setTimeout(r,150));}
await b.close()})();
