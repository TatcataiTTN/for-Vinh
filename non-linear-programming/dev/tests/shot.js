const puppeteer = require('/opt/homebrew/lib/node_modules/@mermaid-js/mermaid-cli/node_modules/puppeteer-core');
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new'});
const p=await b.newPage();await p.setViewport({width:1280,height:1700});
const url=process.argv[2], tag=process.argv[3], slides=(process.argv[4]||'').split(',').filter(Boolean).map(Number);
await p.goto(url,{waitUntil:'networkidle0'});await p.addStyleTag({content:'.topbar{position:static!important}'});
for(const n of slides){await p.evaluate(n=>{const d=document.querySelector('.mdeck');d._go(n-1);d.scrollIntoView();},n);await new Promise(r=>setTimeout(r,400));
 const el=await p.$('.mdeck');await el.screenshot({path:`shots/${tag}_s${n}.png`});}
for(const w of (process.argv[5]||'').split(',').filter(Boolean)){const el=await p.$(`.widget[data-widget="${w}"]`);if(el){await el.scrollIntoView?.();await el.screenshot({path:`shots/${tag}_w_${w}.png`});}}
await b.close();})();
