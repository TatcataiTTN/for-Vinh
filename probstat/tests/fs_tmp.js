const p=require('puppeteer-core');
(async()=>{
const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--no-sandbox']});
const pg=await b.newPage();await pg.setViewport({width:1300,height:800});
await pg.goto(process.argv[2]+'/vi/m05-bien-ngau-nhien/index.html',{waitUntil:'networkidle0'});
await pg.click('.mdeck-fs');await new Promise(r=>setTimeout(r,1000));
console.log(await pg.evaluate(()=>{const d=document.querySelector('.mdeck'),v=d.querySelector('.mdeck-viewport'),s=d.querySelector('.mdeck-slide.active'),bar=d.querySelector('.mdeck-bar');const r=e=>JSON.stringify(e.getBoundingClientRect());const cs=getComputedStyle(d);return {disp:cs.display,dir:cs.flexDirection,vpcs:getComputedStyle(v).flex+'/'+getComputedStyle(v).position,inner:innerHeight,deck:r(d),vp:r(v),slide:r(s),bar:r(bar),font:s.style.fontSize,sh:s.scrollHeight,ch:s.clientHeight,idx:[...d.querySelectorAll('.mdeck-slide')].indexOf(s)}}));
await pg.screenshot({path:'/tmp/fs2.png'});await b.close()})();
