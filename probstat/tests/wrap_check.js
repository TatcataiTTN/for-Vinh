const puppeteer=require('puppeteer-core');
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--no-sandbox']});
const p=await b.newPage();await p.setViewport({width:1000,height:900});
for(const u of ['de-giua-ky','de-giua-ky-2']){await p.goto('http://localhost:18433/vi/'+u+'/index.html',{waitUntil:'networkidle0'});
const r=await p.evaluate(()=>[...document.querySelectorAll('pre')].map(e=>e.scrollWidth>e.clientWidth+1));
console.log(u,'pre tràn ngang:',r.filter(x=>x).length,'/',r.length);
await p.screenshot({path:'/tmp/'+u+'.png',clip:{x:0,y:500,width:1000,height:700}});}
await b.close()})();
