const puppeteer = require('/opt/homebrew/lib/node_modules/@mermaid-js/mermaid-cli/node_modules/puppeteer-core');
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new'});
const base=process.argv[2];const p=await b.newPage();await p.setViewport({width:1280,height:1700});
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
// M3: active set + qp solver
await p.goto(base+'modules/03-quy-hoach-toan-phuong/index.html',{waitUntil:'networkidle0'});
const as=await p.evaluate(async()=>{const w=document.querySelector('[data-widget="active-set-stepper"]');const outs=[];
 for(let i=0;i<8;i++){const n=w.querySelector('#as-next');if(n.disabled)break;n.click();await new Promise(r=>setTimeout(r,60));outs.push(w.querySelector('#as-k').textContent+' | '+w.querySelector('#as-out b').textContent);}
 w.querySelector('#as-p').selectedIndex=1;w.querySelector('#as-p').dispatchEvent(new Event('change'));await new Promise(r=>setTimeout(r,100));
 for(let i=0;i<10;i++){const n=w.querySelector('#as-next');if(n.disabled)break;n.click();await new Promise(r=>setTimeout(r,40));}
 outs.push('BT: '+w.querySelector('#as-k').textContent+' | '+w.querySelector('#as-out b').textContent);return outs;});
console.log(as.join('\n'));
const qp=await p.evaluate(async()=>{const w=document.querySelector('[data-widget="qp-eq-solver"]');const t1=w.querySelector('#qout').innerText;w.querySelector('#qbt').click();await new Promise(r=>setTimeout(r,80));return [t1,w.querySelector('#qout').innerText];});
console.log(qp.join('\n---\n'));
// M2: kkt lab
await p.goto(base+'modules/02-rang-buoc-kkt/index.html',{waitUntil:'networkidle0'});
const kk=await p.evaluate(async()=>{const w=document.querySelector('[data-widget="kkt-lab"]');const res=[];const sel=w.querySelector('#kp');
 for(let i=0;i<sel.options.length;i++){sel.selectedIndex=i;sel.dispatchEvent(new Event('change'));await new Promise(r=>setTimeout(r,60));
  const cand=w.querySelectorAll('#kcand button');for(const c of cand){c.click();await new Promise(r=>setTimeout(r,40));res.push(sel.options[i].text.slice(0,18)+' '+c.textContent+' -> '+[...w.querySelectorAll('#kout .badge')].pop().textContent);}}
 return res;});
console.log(kk.join('\n'));
console.log('errors:',errs);await b.close();})();
