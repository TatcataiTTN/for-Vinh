// Duyệt MỌI trang HTML của site ở 3 độ rộng (360, 768, 1280): lỗi JS/console/HTTP, tràn ngang, công thức KaTeX lỗi, ảnh hỏng.
// node tests/all_pages_check.js [BASE_URL] [thư mục site]
const puppeteer=require('puppeteer-core');const fs=require('fs'),path=require('path');
const BASE=(process.argv[2]||'http://localhost:18432/').replace(/\/?$/,'/');const ROOT=path.resolve(process.argv[3]||path.join(__dirname,'..'));
function walk(d,o=[]){for(const f of fs.readdirSync(d)){if(['node_modules','.git','tests','build','data','_shared','img','drawio'].includes(f))continue;const p=path.join(d,f);const s=fs.statSync(p);if(s.isDirectory())walk(p,o);else if(f==='index.html')o.push(path.relative(ROOT,p))}return o}
(async()=>{const pages=walk(ROOT);const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--no-sandbox']});
let fails=0,checks=0;const bad=[];
for(const w of [360,768,1280]){for(const u of pages){const p=await b.newPage();await p.setViewport({width:w,height:800});const errs=[];p.on('pageerror',e=>errs.push('js '+e.message));p.on('console',m=>{if(m.type()==='error')errs.push('console '+m.text())});p.on('response',r=>{if(r.status()>=400)errs.push('HTTP '+r.status()+' '+r.url().replace(BASE,''))});
 try{await p.goto(BASE+u,{waitUntil:'networkidle0',timeout:30000})}catch(e){errs.push('không tải được '+e.message)}
 const r=await p.evaluate(()=>{const ov=document.documentElement.scrollWidth>innerWidth+2;const wide=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>innerWidth+2&&r.width>0&&!e.closest('.tbwrap,.scroll,pre,.mdeck-slide,table,.katex-display,.pd-formula-math,svg')&&getComputedStyle(e).position!=='fixed'}).slice(0,2).map(e=>e.tagName+'.'+e.className);
  return {ov,wide,kerr:document.querySelectorAll('.katex-error').length,imgs:[...document.images].filter(i=>i.complete&&i.naturalWidth===0&&i.src&&!i.src.startsWith('data:')).map(i=>i.src.split('/').slice(-2).join('/')),h1:document.querySelectorAll('h1').length}});
 checks++;const prob=[];if(errs.length)prob.push('lỗi '+JSON.stringify(errs.slice(0,2)));if(r.ov)prob.push('tràn ngang '+JSON.stringify(r.wide));if(r.kerr)prob.push('KaTeX lỗi '+r.kerr);if(r.imgs.length)prob.push('ảnh hỏng '+r.imgs);if(r.h1!==1)prob.push('h1='+r.h1);
 if(prob.length){fails++;bad.push(w+'px /'+u+': '+prob.join('; '))}await p.close()}}
bad.forEach(x=>console.log('FAIL',x));console.log(pages.length+' trang × 3 độ rộng = '+checks+' lượt duyệt; '+(fails?fails+' lượt có lỗi':'tất cả sạch'));await b.close();process.exit(fails?1:0)})();
