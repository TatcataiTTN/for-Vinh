const puppeteer = require('/opt/homebrew/lib/node_modules/@mermaid-js/mermaid-cli/node_modules/puppeteer-core');
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new'});
const p=await b.newPage();p.on('pageerror',e=>console.log('PAGEERR',e.message));p.on('console',m=>console.log('C',m.type(),m.text().slice(0,200)));
await p.goto(process.argv[2],{waitUntil:'networkidle0'});
console.log(await p.evaluate(()=>({root:!!document.getElementById('code-root'),data:!!document.getElementById('code-data'),cards:document.querySelectorAll('.code-card').length,scripts:[...document.scripts].map(s=>s.src.split('/').pop()||'inline')})));
await b.close();})();
