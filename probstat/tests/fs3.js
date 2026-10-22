const p=require('puppeteer-core');
(async()=>{
const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--no-sandbox']});
const pg=await b.newPage();await pg.setViewport({width:1300,height:800});
await pg.goto('http://localhost:8765/vi/m05-bien-ngau-nhien/index.html',{waitUntil:'networkidle0'});
await pg.click('.mdeck-fs');await new Promise(r=>setTimeout(r,1500));
console.log(await pg.evaluate(()=>{const d=document.querySelector('.mdeck');const o=[];for(const c of d.children){const cs=getComputedStyle(c);o.push(c.className+' h='+c.getBoundingClientRect().height+' flex='+cs.flex+' max='+cs.maxHeight+' disp='+cs.display)}return o.join('\n')+'\n'+getComputedStyle(d).height+' '+document.fullscreenElement.className+' '+innerHeight+' '+screen.height}));
await b.close()})();
