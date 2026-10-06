const puppeteer = require('/opt/homebrew/lib/node_modules/@mermaid-js/mermaid-cli/node_modules/puppeteer-core');
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new'});
const p=await b.newPage();await p.goto(process.argv[2],{waitUntil:'networkidle0'});
const r=await p.evaluate(()=>{const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(/\\\(|\\\[|\\\)/.test(n.nodeValue)&&!n.parentElement.closest('script,.katex')) out.push(n.nodeValue.slice(0,160)+' <'+n.parentElement.tagName+'.'+n.parentElement.className+'>');}return out;});
console.log(r.join('\n'));
const nf=await p.evaluate(()=>{const f=[];document.querySelectorAll('img').forEach(i=>{if(i.complete&&!i.naturalWidth)f.push(i.src)});return f});console.log('broken',nf);
await b.close();})();
