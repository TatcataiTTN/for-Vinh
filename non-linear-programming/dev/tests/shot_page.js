const puppeteer = require('/opt/homebrew/lib/node_modules/@mermaid-js/mermaid-cli/node_modules/puppeteer-core');
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new'});
const p=await b.newPage();await p.setViewport({width:1200,height:1400});await p.goto(process.argv[2],{waitUntil:'networkidle0'});await p.screenshot({path:process.argv[3],fullPage:false});await b.close();})();
