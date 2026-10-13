// Kiểm thử trình duyệt thật: node site_test.js [BASE] [module ids...]
const puppeteer=require('puppeteer-core');const fs=require('fs');const path=require('path');
const BASE=(process.argv[2]||'http://localhost:18432/vi/').replace(/\/?$/,'/');
const mods=JSON.parse(fs.readFileSync(path.join(__dirname,'mods.json')));
const only=process.argv.slice(3);
(async()=>{
 const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--no-sandbox']});
 let fails=0;const log=(ok,m)=>{if(!ok){fails++;console.log('FAIL',m)}};
 async function open(url){const p=await b.newPage();await p.setViewport({width:1100,height:900});const errs=[];p.on('pageerror',e=>errs.push('pageerror '+e.message));
  p.on('console',m=>{if(m.type()==='error')errs.push('console '+m.text())});p.on('response',r=>{if(r.status()>=400)errs.push('HTTP '+r.status()+' '+r.url())});
  await p.goto(url,{waitUntil:'networkidle0'});return [p,errs]}
 for(const m of mods.filter(m=>!only.length||only.includes(m.id))){
  let [p,errs]=await open(BASE+m.slug+'/index.html');
  if(errs.length&&errs[0].startsWith('HTTP 404')&&errs.length===1){console.log('skip (chưa có)',m.id);await p.close();continue}
  const info=await p.evaluate(()=>({slides:document.querySelectorAll('.mdeck-slide').length,sims:document.querySelectorAll('.sim').length,
    simOut:[...document.querySelectorAll('.sim')].map(s=>s.textContent.length>80),simErr:[...document.querySelectorAll('.sim .no')].map(e=>e.textContent).filter(t=>/Lỗi|Chưa có/.test(t)),
    quiz:document.querySelectorAll('#q-'+location.pathname.split('/').slice(-2)[0].slice(0,3)+' .qitem').length||document.querySelectorAll('.quiz .qitem').length,
    katexErr:document.querySelectorAll('.katex-error').length,katex:document.querySelectorAll('.katex').length,
    imgSrcs:[...document.querySelectorAll('img')].map(i=>i.src)}));
  info.imgs=0;for(const u of info.imgSrcs){const ok=await p.evaluate(async u=>{try{const r=await fetch(u);return r.ok&&(await r.blob()).size>1000}catch(e){return false}},u);if(!ok)info.imgs++}
  log(info.slides>=15,m.id+' slides '+info.slides);log(info.quiz===10,m.id+' quiz '+info.quiz);log(info.simOut.every(x=>x),m.id+' sim rỗng '+JSON.stringify(info.simOut));log(info.simErr.length===0,m.id+' sim lỗi '+info.simErr);
  log(info.katexErr===0,m.id+' katex-error '+info.katexErr);log(info.katex>0,m.id+' ít công thức '+info.katex);log(info.imgs===0,m.id+' ảnh vỡ '+info.imgs);
  const q=await p.evaluate(()=>{const it=document.querySelector('.quiz .qitem');it.querySelector('.opt').click();const shown=it.querySelector('.explain').classList.contains('show');
    [...it.querySelectorAll('button')].find(x=>x.textContent.includes('Làm lại câu này')).click();return {shown,cleared:!it.querySelector('.opt.correct,.opt.wrong')}});
  log(q.shown&&q.cleared,m.id+' quiz explain/reset '+JSON.stringify(q));
  await p.evaluate(()=>{for(let i=0;i<4;i++)document.querySelector('.mdeck-next').click()});
  log((await p.evaluate(()=>document.querySelector('.mdeck-count').textContent)).startsWith('5/'),m.id+' deck nav');
  log(errs.length===0,m.id+' lỗi console: '+errs.slice(0,3).join(' | '));await p.close();
  let [p2,e2]=await open(BASE+m.slug+'/luyen-tap/index.html');
  const bk=await p2.evaluate(()=>{const D=JSON.parse(document.getElementById('bank-data').textContent);const it=document.querySelectorAll('#bank .qitem')[0];it.querySelectorAll('.opt')[0].click();
    const ex=it.querySelector('.explain').classList.contains('show')&&it.querySelector('.explain').textContent.length>15;[...it.querySelectorAll('button')].find(x=>x.textContent.includes('Làm lại câu này')).click();
    const cleared=!document.querySelector('#bank .qitem .opt.correct,#bank .qitem .opt.wrong');
    return {n:document.querySelectorAll('#bank .qitem').length,ex,cleared,items:D.items.length,ess:D.essays.length,goc:D.items.filter(x=>x.origin==='goc').length,srcs:D.items.every(x=>x.src&&x.src.length>3),exp:D.items.every(x=>x.explain&&x.explain.length>10)}});
  log(bk.n>=10&&bk.ex&&bk.cleared,m.id+' bank '+JSON.stringify(bk));log(bk.items>=100&&bk.items<=300,m.id+' số câu '+bk.items);log(bk.srcs&&bk.exp,m.id+' thiếu nguồn/giải thích');log(e2.length===0,m.id+' bank console '+e2.slice(0,2));
  console.log(m.id.padEnd(5),'slides',info.slides,'| MCQ',bk.items,'(gốc '+bk.goc+') | tự luận',bk.ess,'| sims',info.sims,'| katex',info.katex);await p2.close();
 }
 for(const u of ['index.html','luyen-de/index.html','bang-tra/index.html','tai-lieu/index.html']){const [p,e]=await open(BASE+u);const t=await p.evaluate(()=>document.body.textContent.length);log(t>300,u+' rỗng');log(e.length===0,u+' lỗi '+e.slice(0,2));
  if(u.startsWith('bang-tra')){const r=await p.evaluate(()=>document.querySelector('#phi').textContent);log(r==='0.9332','bảng tra Φ(1.5)='+r)}await p.close()}
 console.log(fails?('TỔNG: '+fails+' lỗi'):'TỔNG: tất cả kiểm thử đạt');await b.close();process.exit(fails?1:0);
})();
