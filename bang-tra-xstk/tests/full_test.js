// Kiểm thử ĐẦY ĐỦ site Học tra bảng XSTK: node tests/full_test.js [BASE]
// (1) mọi ô bảng trên màn hình = số in trong giáo trình; (2) liên kết, id, nhãn; (3) tra thử mọi chế độ + trường hợp biên; (4) nội suy JS = Python;
// (5) giao diện sáng/tối + độ tương phản; (6) in; (7) điện thoại/máy tính bảng; (8) luyện tập lưu và làm lại.
const puppeteer=require('../../probstat/tests/node_modules/puppeteer-core');const fs=require('fs'),path=require('path');
const BASE=(process.argv[2]||'http://localhost:18434/').replace(/\/?$/,'/');
const PR=JSON.parse(fs.readFileSync(path.join(__dirname,'printed.json'))),IR=JSON.parse(fs.readFileSync(path.join(__dirname,'interp_ref.json')));
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--no-sandbox']});
let fails=0,oks=0;const log=(ok,m)=>{if(!ok){fails++;console.log('FAIL',m)}else{oks++;if(process.env.V)console.log('ok  ',m)}};
const PAGES=['','chuan-tac/','student/','chi-binh-phuong/','luyen-tra/','de-that/','in-bang/'];
async function open(u,w,h){const p=await b.newPage();await p.setViewport({width:w||1100,height:h||900});const errs=[];p.on('pageerror',e=>errs.push('pageerror '+e.message));p.on('console',m=>{if(m.type()==='error')errs.push('console '+m.text())});p.on('response',r=>{if(r.status()>=400)errs.push('HTTP '+r.status()+' '+r.url())});await p.goto(BASE+u,{waitUntil:'networkidle0'});return [p,errs]}
const mn=s=>String(s).replace(/-/g,'−');
const fill=async(h,v)=>{await h.evaluate(e=>{e.focus();e.select()});await h.press('Backspace');await h.type(String(v))};

// ── (1) bảng trên màn hình = số in
{const [p,e]=await open('in-bang/');
 const r=await p.evaluate((PR)=>{const bad=[];let n=0;
  document.querySelectorAll('#tbl-a7 td[data-k]').forEach(c=>{n++;const k=c.getAttribute('data-k');if(c.textContent!==PR.A7[k])bad.push(['A7',k,c.textContent,PR.A7[k]])});
  const a8=document.querySelectorAll('#tbl-a8 td[data-p]');const seen={};a8.forEach(c=>{if(c.classList.contains('zc'))return;const P=c.getAttribute('data-p'),col=+c.getAttribute('data-c');seen[P]=seen[P]||[];seen[P][col]=c.textContent});
  Object.keys(PR.A8).forEach(P=>{n+=2;const s=seen[P];if(!s){bad.push(['A8 thiếu hàng',P]);return}const pa=PR.A8[P];if(s[0].replace('−','')!==pa[0]||s[1]!==pa[1])bad.push(['A8',P,s,pa]);const neg=+P<50;if(neg!==s[0].startsWith('−')&&!(+P===50))bad.push(['A8 dấu',P,s[0]])});
  [['a9',PR.A9],['a10',PR.A10]].forEach(([id,M])=>{document.querySelectorAll('#tbl-'+id+' td[data-f]').forEach(c=>{n++;const k=c.getAttribute('data-f')+'|'+c.getAttribute('data-df');if(M[k]===undefined)bad.push([id,'không có trong bản in',k]);else if(c.textContent!==M[k]&&!(id==='a9'&&k==='0.95|inf'))bad.push([id,k,c.textContent,M[k]])})});
  return {n,bad,a8rows:Object.keys(seen).length,a9:document.querySelectorAll('#tbl-a9 td[data-f]').length,a10:document.querySelectorAll('#tbl-a10 td[data-f]').length}},PR);
 log(r.bad.length===0,'(1) bảng hiển thị = số in: '+r.n+' ô so sánh, lệch '+r.bad.length+' '+JSON.stringify(r.bad.slice(0,4)));
 log(r.a8rows===118&&r.a9===300&&r.a10===296,'(1) số ô: A8 '+r.a8rows+' hàng, A9 '+r.a9+', A10 '+r.a10);
 // ngoại lệ đã biết: ô (∞; 0.95) in 1.65
 const x=await p.$eval('#tbl-a9 td[data-f="0.95"][data-df="inf"]',c=>c.textContent);log(x==='1.65','(1) ô (∞; 0.95) = '+x+' đúng như bản in');
 await p.close()}

// ── (2) liên kết, id, nhãn
{const seen=new Set();let total=0,dead=[],anchors=[],dupid=[],nolabel=[],errsAll=[];
 for(const u of PAGES){const [p,e]=await open(u);errsAll.push(...e.map(x=>u+' '+x));
  const info=await p.evaluate(()=>{const ids=[...document.querySelectorAll('[id]')].map(x=>x.id);const dup=ids.filter((x,i)=>ids.indexOf(x)!==i);
   const inputs=[...document.querySelectorAll('input,select')].filter(i=>!(i.getAttribute('aria-label')||i.closest('label')||(i.id&&document.querySelector('label[for="'+i.id+'"]'))));
   return {links:[...document.querySelectorAll('a[href]')].map(a=>a.href),dup,nolabel:inputs.map(i=>i.outerHTML.slice(0,60)),title:document.title,h1:document.querySelectorAll('h1').length,lang:document.documentElement.lang}});
  if(info.dup.length)dupid.push(u+':'+info.dup);if(info.nolabel.length)nolabel.push(u+':'+info.nolabel);
  log(info.h1===1&&info.lang==='vi'&&info.title.includes('Học tra bảng'),'(2) /'+u+' có 1 h1, lang=vi, title "'+info.title.slice(0,40)+'"');
  for(const l of info.links){const clean=l.split('#')[0];if(!l.startsWith(BASE)&&!l.includes('tatcataittn.github.io')&&!l.startsWith('http://localhost'))continue;
   if(seen.has(l))continue;seen.add(l);total++;
   if(l.startsWith('http://localhost')&&new URL(l).pathname.startsWith('/probstat/')){const f=path.join(__dirname,'..','..',new URL(l).pathname);if(!fs.existsSync(f))dead.push(l+' (tệp '+f+')');continue}
   const pg=await b.newPage();const r=await pg.goto(clean,{waitUntil:'domcontentloaded'});if(r.status()>=400)dead.push(l);
   if(l.includes('#')){const id=l.split('#')[1];const ok=await pg.evaluate(id=>!!document.getElementById(id),id);if(!ok)anchors.push(l)}await pg.close()}
  await p.close()}
 log(dead.length===0,'(2) '+total+' liên kết khác nhau, chết: '+JSON.stringify(dead));log(anchors.length===0,'(2) neo # tồn tại: '+JSON.stringify(anchors));
 log(dupid.length===0,'(2) id trùng: '+JSON.stringify(dupid));log(nolabel.length===0,'(2) ô nhập thiếu nhãn: '+JSON.stringify(nolabel));log(errsAll.length===0,'(2) lỗi console/HTTP: '+JSON.stringify(errsAll))}

// ── (3) tra thử: mọi chế độ + biên
{const [p,e]=await open('chuan-tac/');
 const go=async(w,vals,mode)=>{if(mode){await p.select(w+' select',mode)}const ins=await p.$$(w+' input');for(let i=0;i<vals.length;i++){await fill(ins[i],vals[i])}await p.click(w+' .btn');return p.$eval(w+' .lkout',x=>x.textContent)};
 const w7='[data-lk="a7"]',w8='[data-lk="a8"]';let t;
 t=await go(w7,['abc']);log(t.includes('Nhập một số'),'(3) A7 chữ → báo nhập số');
 t=await go(w7,['']);log(t.includes('Nhập một số'),'(3) A7 rỗng → báo nhập số');
 t=await go(w7,['0']);log(t.includes('0.5000'),'(3) A7 z=0 → 0.5000');
 t=await go(w7,['3']);log(t.includes('0.9987'),'(3) A7 z=3 → 0.9987 (biên bảng)');
 t=await go(w7,['3.5']);log(/≈ 1\b/.test(t)||t.includes('vượt bảng'),'(3) A7 z=3.5 → ≈ 1 (ngoài bảng)');
 t=await go(w7,['-3.5']);log(t.includes('vượt bảng'),'(3) A7 z=−3.5 → ngoài bảng');
 t=await go(w7,['1,23']);log(t.includes('0.8907'),'(3) A7 dấu phẩy 1,23 → 0.8907');
 t=await go(w7,['−1.00']);log(t.includes('0.1587'),'(3) A7 dấu trừ Unicode −1.00 → 0.1587');
 t=await go(w7,['0.005']);log(t.includes('làm tròn'),'(3) A7 z=0.005 có ghi chú làm tròn');
 t=await go(w8,['0'],'alpha');log(t.includes('Nhập số phần trăm'),'(3) A8 α=0 → báo lỗi');
 t=await go(w8,['100'],'alpha');log(t.includes('Nhập số phần trăm'),'(3) A8 α=100 → báo lỗi');
 t=await go(w8,['x'],'alpha');log(t.includes('Nhập số phần trăm'),'(3) A8 chữ → báo lỗi');
 t=await go(w8,['50'],'P');log(t.includes('0.000'),'(3) A8 P=50 → z=0');
 t=await go(w8,['99.99'],'P');log(t.includes('3.719'),'(3) A8 P=99.99 → 3.719');
 t=await go(w8,['1'],'P');log(t.includes('−2.326'),'(3) A8 P=1 → −2.326 (dấu âm)');
 t=await go(w8,['0.5'],'alpha');log(t.includes('2.576'),'(3) A8 α=0.5% → hàng 99.5 → 2.576');
 t=await go(w8,['2.5'],'alpha');log(t.includes('1.960'),'(3) A8 α=2.5% → hàng 97.5 → 1.960');
 t=await go(w8,['99.995'],'P');log(t.includes('Ngoài phạm vi'),'(3) A8 P=99.995 → ngoài phạm vi');
 t=await go(w8,['0.5'],'P');log(t.includes('Ngoài phạm vi'),'(3) A8 P=0.5 → ngoài phạm vi');
 log(e.length===0,'(3) trang chuẩn tắc không lỗi JS: '+JSON.stringify(e));await p.close()}
{const [p,e]=await open('student/');const w='[data-lk="a9"]';
 const go=async(mode,df,v)=>{await p.select(w+' select',mode);const ins=await p.$$(w+' input');await fill(ins[0],df);await fill(ins[1],v);await p.click(w+' .btn');return p.$eval(w+' .lkout',x=>x.textContent)};
 let t;
 t=await go('F','0','0.95');log(t.includes('Nhập bậc tự do'),'(3) A9 df=0 → báo lỗi');
 t=await go('F','abc','0.95');log(t.includes('Nhập bậc tự do'),'(3) A9 df chữ → báo lỗi');
 t=await go('F','9','1.2');log(t.includes('F phải nằm'),'(3) A9 F=1.2 → báo lỗi');
 t=await go('F','9','0.3');log(t.includes('Ngoài phạm vi'),'(3) A9 F=0.3 → ngoài phạm vi bảng');
 t=await go('F','9','0.9995');log(t.includes('Ngoài phạm vi'),'(3) A9 F=0.9995 → ngoài phạm vi');
 t=await go('F','∞','0.975');log(t.includes('1.96'),'(3) A9 df=∞ F=0.975 → 1.96');
 t=await go('F','vô cùng','0.975');log(t.includes('1.96'),'(3) A9 df="vô cùng" → 1.96');
 t=await go('F','1','0.999');log(t.includes('318.3')||t.includes('318.31'),'(3) A9 (1; 0.999) → 318.3');
 t=await go('F','500','0.95');log(t.includes('1.65')||t.includes('1.648'),'(3) A9 df=500 (>200) → gần 1.65: '+t.slice(-90));
 t=await go('F','5','0.5');log(t.includes('0.00'),'(3) A9 F=0.5 → 0.00');
 t=await go('alpha','5','5');log(t.includes('2.02'),'(3) A9 α=5% df=5 → F=0.95 → 2.02');
 t=await go('gamma','20','99');log(t.includes('2.85'),'(3) A9 γ=99% df=20 → F=0.995 → 2.85');
 // nội suy: JS = Python
 let bad=0,n=0;for(const [df,F,ref] of IR){const tx=await go('F',df,F);const m=/Kết quả: t ≈ ([\d.]+)/.exec(tx);n++;if(!m||Math.abs(+m[1]-ref)>0.0006){bad++;if(bad<4)console.log('  lệch',df,F,ref,m&&m[1])}}
 log(bad===0,'(3) nội suy A9 của JS = Python trên '+n+' ca (lệch '+bad+')');
 log(e.length===0,'(3) trang Student không lỗi JS: '+JSON.stringify(e));await p.close()}
{const [p,e]=await open('chi-binh-phuong/');const w='[data-lk="a10"]';
 const go=async(m,F)=>{const ins=await p.$$(w+' input');await fill(ins[0],m);await fill(ins[1],F);await p.click(w+' .btn');return p.$eval(w+' .lkout',x=>x.textContent)};let t;
 t=await go('0','0.95');log(t.includes('Nhập m'),'(3) A10 m=0 → báo lỗi');
 t=await go('1','0.005');log(t.includes('0.00'),'(3) A10 (1; 0.005) → 0.00');
 t=await go('100','0.995');log(t.includes('140.2'),'(3) A10 (100; 0.995) → 140.2');
 t=await go('101','0.95');log(/124\.|125\./.test(t),'(3) A10 m=101 → xấp xỉ ½(h+z)²: '+t.slice(-70));
 t=await go('150','0.5');log(t.includes('Bảng A10 chỉ có'),'(3) A10 F không có trong bảng → giải thích');
 t=await go('35','0.95');log(t.includes('Bảng A10 chỉ có')&&t.includes('49.8'),'(3) A10 m=35 không có cột → báo + giá trị máy tính 49.8');
 log(e.length===0,'(3) trang χ² không lỗi JS: '+JSON.stringify(e));await p.close()}

// ── (5) sáng/tối + tương phản
{const [p]=await open('student/');
 const lum=c=>{const [r,g,b]=c.match(/\d+(\.\d+)?/g).slice(0,3).map(Number).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*r+.7152*g+.0722*b};
 const ratio=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
 async function measure(){return p.evaluate(()=>{const gs=(sel,prop)=>{const e=document.querySelector(sel);return e?getComputedStyle(e)[prop]:null};const bgOf=sel=>{let e=document.querySelector(sel);while(e){const c=getComputedStyle(e).backgroundColor;if(c&&c!=='rgba(0, 0, 0, 0)'&&c!=='transparent')return c;e=e.parentElement}return 'rgb(255,255,255)'};
   const pairs={body:['main p',bgOf('main p')],muted:['.lead',bgOf('.lead')],callout:['.callout',bgOf('.callout')],th:['table.t th',bgOf('table.t th')],cellhl:['#tbl-a9 td',bgOf('#tbl-a9 td')],link:['main a',bgOf('main a')],note:['.note',bgOf('.note')]};
   const out={};for(const k in pairs){const [sel,bg]=pairs[k];const col=gs(sel,'color');if(col)out[k]=[col,bg]}return out})}
 for(const th of ['light','dark']){await p.evaluate(t=>document.documentElement.setAttribute('data-theme',t),th);const m=await measure();const bad=[];for(const k in m){const r=ratio(m[k][0],m[k][1]);if(r<4.5)bad.push(k+'='+r.toFixed(2))}
  log(bad.length===0,'(5) tương phản chữ/nền theme '+th+' ≥ 4.5: '+(bad.join(', ')||'đạt'))}
 // nút đổi theme + nhớ lựa chọn
 const before=await p.evaluate(()=>document.documentElement.getAttribute('data-theme'));await p.click('#themebtn');const after=await p.evaluate(()=>document.documentElement.getAttribute('data-theme'));
 await p.reload({waitUntil:'networkidle0'});const kept=await p.evaluate(()=>document.documentElement.getAttribute('data-theme'));
 log(before!==after&&kept===after,'(5) nút đổi theme: '+before+' → '+after+', sau khi tải lại vẫn '+kept);await p.close()}

// ── (6) in
{const [p]=await open('in-bang/');await p.emulateMediaType('print');
 const r=await p.evaluate(()=>({hdr:getComputedStyle(document.querySelector('header.top')).display,wraps:[...document.querySelectorAll('.tbwrap')].map(w=>[w.scrollHeight,w.clientHeight,getComputedStyle(w).maxHeight]),bg:getComputedStyle(document.body).backgroundColor}));
 log(r.hdr==='none','(6) in: ẩn thanh trên cùng');log(r.wraps.every(w=>w[2]==='none'&&w[0]<=w[1]+2),'(6) in: bảng không bị cắt bởi khung cuộn '+JSON.stringify(r.wraps));log(r.bg==='rgb(255, 255, 255)','(6) in: nền trắng');
 const pdf=await p.pdf({format:'A4',printBackground:false});log(pdf.length>20000,'(6) xuất được PDF ('+Math.round(pdf.length/1024)+' KB)');
 const tmp=require('os').tmpdir()+'/bt_print_test.pdf';fs.writeFileSync(tmp,pdf);const pages=+/Pages:\s+(\d+)/.exec(require('child_process').execFileSync('pdfinfo',[tmp]).toString())[1];log(pages>=4&&pages<=20,'(6) PDF có '+pages+' trang (4 bảng, mỗi bảng một trang)');await p.close()}

// ── (7) điện thoại, máy tính bảng
for(const w of [360,390,768,1440]){let bad=[];for(const u of PAGES){const [p]=await open(u,w,800);const ov=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2);if(ov)bad.push(u);
  const clip=await p.evaluate(()=>[...document.querySelectorAll('.lk input,.qbox input')].some(i=>i.getBoundingClientRect().right>innerWidth));if(clip)bad.push(u+' ô nhập tràn');await p.close()}
 log(bad.length===0,'(7) rộng '+w+'px: không tràn ngang trên 7 trang '+JSON.stringify(bad))}

// ── (8) luyện tập: lọc, lưu, làm lại
{const [p]=await open('luyen-tra/');const QS=await p.evaluate(()=>window.QUESTIONS);
 const counts={all:QS.length};['a7','a8','a9','a10'].forEach(k=>counts[k]=QS.filter(q=>q.t===k).length);
 const lab={a7:'A7 Φ(z)',a8:'A8 z, U_α',a9:'A9 Student',a10:'A10 χ²'};
 for(const k of ['a7','a8','a9','a10']){await p.evaluate(l=>[...document.querySelectorAll('.row button')].find(x=>x.textContent===l).click(),lab[k]);const s=await p.$eval('.quiz-score',x=>x.textContent);log(s.includes('Nhóm này: '+counts[k]+' câu'),'(8) tab '+k+': '+s.slice(0,30)+' khớp '+counts[k]);
  const q=await p.$eval('.qtxt',x=>x.textContent);const id=+/Câu (\d+)\./.exec(q)[1];log(QS.find(x=>x.id===id).t===k,'(8) tab '+k+' chỉ ra câu thuộc nhóm '+k)}
 await p.evaluate(l=>[...document.querySelectorAll('.row button')].find(x=>x.textContent===l).click(),'Tất cả');
 // làm 3 câu đúng + 2 sai rồi tải lại: tiến độ còn
 let right=0,wrong=0;for(let i=0;i<5;i++){const q=await p.$eval('.qtxt',x=>x.textContent);const id=+/Câu (\d+)\./.exec(q)[1];const Q=QS.find(x=>x.id===id);const ok=i<3;const inp=await p.$('.qbox input');await fill(inp,String(ok?Q.a:Q.a+777));
  if(i===0){await p.keyboard.press('Enter')}else{await p.click('.qbox .btn:not(.alt)')}
  const fb=await p.$eval('.fb',x=>x.textContent);if(ok&&fb.includes('Đúng'))right++;if(!ok&&fb.includes('Sai'))wrong++;await p.click('.fb .btn')}
 log(right===3&&wrong===2,'(8) 3 đúng, 2 sai được chấm đúng (Enter hoặc nút): '+right+'/'+wrong);
 await p.reload({waitUntil:'networkidle0'});const s2=await p.$eval('.quiz-score',x=>x.textContent);log(s2.includes('đúng 3')&&s2.includes('sai 2'),'(8) tải lại: tiến độ giữ nguyên → '+s2);
 await p.evaluate(()=>[...document.querySelectorAll('.row button')].find(x=>x.textContent.includes('Làm lại')).click());const s3=await p.$eval('.quiz-score',x=>x.textContent);log(s3.includes('đúng 0')&&s3.includes('sai 0'),'(8) nút làm lại xoá tiến độ nhóm → '+s3);
 // gợi ý
 await p.click('.qbox .btn.alt');const hint=await p.$eval('.fb',x=>x.textContent);log(hint.includes('💡'),'(8) nút gợi ý hiện gợi ý');await p.close()}

console.log('\n'+(fails?('TỔNG: '+fails+' lỗi / '+(oks+fails)+' kiểm tra'):'TỔNG: tất cả '+oks+' kiểm tra đạt'));await b.close();process.exit(fails?1:0)})();
