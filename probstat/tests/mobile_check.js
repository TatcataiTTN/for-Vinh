// Kiểm tra giao diện điện thoại (390×844): không tràn ngang, menu không dính (không chiếm màn hình), tiêu đề neo không bị che.
// node tests/mobile_check.js <URL trang> [<URL trang> ...]
const puppeteer=require('puppeteer-core');
const urls=process.argv.slice(2);if(!urls.length){console.log('Cần ít nhất một URL');process.exit(2)}
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--no-sandbox']});let bad=0;
for(const u of urls){const p=await b.newPage();await p.setViewport({width:390,height:844,deviceScaleFactor:2,isMobile:true,hasTouch:true});await p.goto(u,{waitUntil:'networkidle0'});
 const r=await p.evaluate(()=>{const h=document.querySelector('header.top');const pos=h?getComputedStyle(h).position:'(không có)';
  const hh=h?h.getBoundingClientRect().height:0;window.scrollTo(0,600);const stuck=h?h.getBoundingClientRect().top>-1&&pos==='sticky':false;
  return {sw:document.documentElement.scrollWidth,W:innerWidth,pos,hh:Math.round(hh),stuck}});
 const ok=r.sw<=r.W+1&&r.pos!=='sticky';if(!ok)bad++;
 console.log((ok?'ok  ':'FAIL')+' '+u.replace(/^https?:\/\/[^/]+/,'')+' | scrollWidth '+r.sw+'/'+r.W+' | menu position='+r.pos+' ('+r.hh+'px cao)');await p.close()}
await b.close();process.exit(bad?1:0)})();
