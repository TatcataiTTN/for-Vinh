const p=require('puppeteer-core');
(async()=>{
const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--no-sandbox']});
const pg=await b.newPage();await pg.setViewport({width:1400,height:850});
const errs=[];pg.on('pageerror',e=>errs.push(String(e)));
await pg.goto(process.argv[2],{waitUntil:'networkidle0'});
const go=async n=>{for(let i=0;i<n;i++){await pg.click('.mdeck-next')}};
await go(4);
await pg.screenshot({path:'/tmp/a_normal.png'});
await pg.click('.mdeck-fs');await new Promise(r=>setTimeout(r,800));
const info=await pg.evaluate(()=>{const s=document.querySelector('.mdeck-slide.active');return {fs:!!document.fullscreenElement,font:s.style.fontSize,sh:s.scrollHeight,ch:s.clientHeight,bar:document.querySelector('.mdeck-bar').getBoundingClientRect().bottom,inner:innerHeight,katexErr:document.querySelectorAll('.katex-error').length}});
console.log(info);
await pg.screenshot({path:'/tmp/a_fs.png'});
await pg.keyboard.press('ArrowRight');await new Promise(r=>setTimeout(r,400));
await pg.screenshot({path:'/tmp/a_fs2.png'});
console.log(errs);await b.close()})();
