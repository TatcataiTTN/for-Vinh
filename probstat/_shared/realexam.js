/* Đề giữa kỳ thật + mã đề mới: điền đáp số, chấm tức thì có giải thích, tự luận có ô số + lời giải từng bước, đồng hồ 60 phút, làm lại. Chạy 100% trong trình duyệt. */
(function(){
var root=document.getElementById('realexam');if(!root)return;
var D=JSON.parse(document.getElementById('realexam-data').textContent);
var KEY='probstat-realexam-best',best={};try{best=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
function save(){try{localStorage.setItem(KEY,JSON.stringify(best))}catch(e){}}
var cur=0,left=3600,timer=null,graded=false;
function el(t,c,txt){var e=document.createElement(t);if(c)e.className=c;if(txt!==undefined)e.textContent=txt;return e}
function fmt(s){return Math.floor(s/60)+':'+('0'+(s%60)).slice(-2)}
function num(s,th){if(s==null)return NaN;s=String(s).trim().replace(/\s+/g,'');if(!s)return NaN;
  if(th&&/^[1-9]\d{0,2}([.,]\d{3})+$/.test(s))s=s.replace(/[.,]/g,'');
  s=s.replace(',','.');return /^[-+]?\d*\.?\d+(e[-+]?\d+)?$/i.test(s)?parseFloat(s):NaN}
function show(x){if(Number.isInteger(x))return String(x);return String(parseFloat(x.toFixed(4)))}
function ok(v,a,t){return !isNaN(v)&&Math.abs(v-a)<=(t||0)+1e-9}
function sel(){var s=el('select');s.setAttribute('aria-label','Chọn mã đề');
  var g1=el('optgroup'),g2=el('optgroup');g1.label='Mã đề thật HK2.2 2025–2026';g2.label='Mã đề mới (cùng mẫu, số liệu khác)';
  D.forEach(function(d,i){var o=el('option',null,d.code+(best[d.code]!=null?'  ✓ '+best[d.code]:''));o.value=i;if(i===cur)o.selected=true;(d.real?g1:g2).appendChild(o)});
  s.appendChild(g1);s.appendChild(g2);s.onchange=function(){go(+s.value)};return s}
function go(i){cur=i;left=3600;graded=false;render()}
function render(){
  clearInterval(timer);timer=null;root.innerHTML='';var d=D[cur];
  var bar=el('div','sim');bar.innerHTML='<div class="simh">Mã đề '+d.code+(d.real?' · đề thật':' · đề mới cùng mẫu')+' · 8 câu điền đáp số (4đ) + 1 tự luận (6đ) · 60 phút</div>';
  var row=el('div','row');row.appendChild(sel());
  var pv=el('button','btn alt','◀');pv.title='Mã đề trước';pv.onclick=function(){go((cur+D.length-1)%D.length)};
  var nx=el('button','btn alt','▶');nx.title='Mã đề sau';nx.onclick=function(){go((cur+1)%D.length)};
  var rd=el('button','btn alt','🎲 Ngẫu nhiên');rd.onclick=function(){go(Math.floor(Math.random()*D.length))};
  [pv,nx,rd].forEach(function(b){b.style.marginLeft='6px';row.appendChild(b)});bar.appendChild(row);
  var tm=el('span','quiz-score','Đồng hồ: '+fmt(left));tm.style.marginRight='10px';var st=el('button','btn alt','⏱ Bắt đầu tính giờ');
  st.onclick=function(){if(timer){clearInterval(timer);timer=null;st.textContent='⏱ Tiếp tục';return}
    timer=setInterval(function(){left--;tm.textContent='Đồng hồ: '+fmt(left);if(left<=0){clearInterval(timer);grade()}},1000);st.textContent='⏸ Tạm dừng'};
  var gb=el('button','btn','Chấm bài');gb.style.marginLeft='6px';gb.onclick=grade;
  var rb=el('button','btn alt','↺ Làm lại mã đề này');rb.style.marginLeft='6px';rb.onclick=function(){go(cur)};
  var ln=el('div');ln.style.marginTop='8px';[tm,st,gb,rb].forEach(function(b){ln.appendChild(b)});bar.appendChild(ln);root.appendChild(bar);
  d.stems.forEach(function(q,i){var box=el('div','qitem');var t=el('div','qtxt');t.style.fontWeight='600';t.textContent='Câu '+(i+1)+' (0,5 điểm). '+q;box.appendChild(t);
    var inp=el('input');inp.type='text';inp.inputMode='decimal';inp.className='rx-in';inp.id='rx'+i;inp.placeholder='Đáp số';inp.autocomplete='off';
    inp.onkeydown=function(e){if(e.key==='Enter'){var n=document.getElementById('rx'+(i+1));if(n)n.focus()}};
    var w=el('div');w.style.margin='6px 0';w.appendChild(inp);box.appendChild(w);var fb=el('div','explain');fb.id='rf'+i;box.appendChild(fb);root.appendChild(box)});
  var eb=el('div','qitem');var et=el('div','qtxt');et.style.fontWeight='600';et.textContent='Câu 9 (6 điểm), tự luận. '+d.essay;eb.appendChild(et);
  d.parts.forEach(function(p){var pp=el('div',null,p);pp.style.margin='4px 0';eb.appendChild(pp)});
  var g=el('div','rx-grid');
  [['e_xb','x̄ ='],['e_s2','s² ='],['e_b0','(b) cận dưới'],['e_b1','(b) cận trên'],['e_c0','(c) cận dưới'],['e_c1','(c) cận trên']].forEach(function(p){
    var l=el('label',null,p[1]+' ');var i=el('input');i.type='text';i.inputMode='decimal';i.id=p[0];i.className='rx-in';i.autocomplete='off';l.appendChild(i);g.appendChild(l)});
  eb.appendChild(g);var ef=el('div','explain');ef.id='ref';eb.appendChild(ef);
  var sol=el('details');sol.id='resol';var sm=el('summary',null,'📖 Xem lời giải từng bước của câu 9 (làm xong hãy mở)');sol.appendChild(sm);var sb=el('div');sb.innerHTML=d.esol;sol.appendChild(sb);eb.appendChild(sol);root.appendChild(eb);
  var res=el('div','quiz-score');res.id='rres';root.appendChild(res);
}
function grade(){
  if(graded)return;graded=true;clearInterval(timer);timer=null;var d=D[cur],sc=0;
  d.ans.forEach(function(a,i){var inp=document.getElementById('rx'+i),fb=document.getElementById('rf'+i),v=num(inp.value,Number.isInteger(a)),right=ok(v,a,d.tol[i]);
    if(right)sc+=0.5;inp.disabled=true;fb.className='explain show';fb.innerHTML='';
    var h=el('div',null,right?'✅ Đúng — đáp số '+show(a):(isNaN(v)?'⚪ Chưa trả lời — đáp số: ':'❌ Sai — đáp số đúng: ')+(right?'':show(a)));h.style.fontWeight='600';fb.appendChild(h);fb.appendChild(el('div',null,d.expl[i]))});
  var e=d.eans,t=d.etol,pts=0,out=[];
  var va=num(document.getElementById('e_xb').value),vb=num(document.getElementById('e_s2').value);
  var a1=ok(va,e.xb,t.xb),a2=ok(vb,e.s2,t.s2);pts+=(a1?1:0)+(a2?1:0);out.push('(a) x̄ '+(a1?'✅':'❌')+' '+show(e.xb)+'; s² '+(a2?'✅':'❌')+' '+show(e.s2)+' → '+((a1?1:0)+(a2?1:0))+'/2đ');
  function iv(k,id,tol,lab){var l=num(document.getElementById(id+'0').value),h=num(document.getElementById(id+'1').value),n=(ok(l,e[k][0],tol)?1:0)+(ok(h,e[k][1],tol)?1:0);pts+=n;out.push(lab+' '+(n===2?'✅':n===1?'🟡':'❌')+' ('+show(e[k][0])+'; '+show(e[k][1])+') → '+n+'/2đ')}
  iv('b','e_b',t.b,'(b)');iv('c','e_c',t.c,'(c)');
  var ef=document.getElementById('ref');ef.className='explain show';ef.innerHTML='';ef.appendChild(el('div',null,'Chấm phần số liệu câu 9 (thang gợi ý 2đ + 2đ + 2đ; thang thật do giảng viên quyết định, bài làm đầy đủ còn được điểm trình bày):'));out.forEach(function(x){ef.appendChild(el('div',null,x))});
  document.getElementById('resol').open=true;
  var total=sc+pts;var r=document.getElementById('rres');
  r.textContent='Kết quả ước tính: phần I '+sc.toFixed(1)+'/4, câu 9 '+pts+'/6 → '+total.toFixed(1)+'/10 điểm.';
  if(best[d.code]==null||total>best[d.code]){best[d.code]=+total.toFixed(1);save()}r.scrollIntoView({behavior:'smooth',block:'center'});
}
render();
})();
