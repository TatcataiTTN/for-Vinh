(function(){'use strict';
var SL=window.SL,PS=SL.PS,esc=SL.esc,frame=SL.frame,$=SL.$,nums=SL.nums,W=window.SIM_W;
function F(x,d){return PS.fmt(x,d===undefined?4:d)}
function rnorm(){var u=0,v=0;while(!u)u=Math.random();while(!v)v=Math.random();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v)}
W.mle=function(root){
  frame(root,'Hàm hợp lý và ước lượng hợp lý cực đại (MLE)',
   '<div class="row"><label>Mô hình: <select id="m"><option value="exp">Mũ f(x) = θe^(−θx) → θ̂ = n/Σx</option><option value="geo">Hình học f(x) = p(1−p)^(x−1) → p̂ = n/Σx</option><option value="poi">Poisson(μ) → μ̂ = x̄</option><option value="ber">Bernoulli(p) (0/1) → p̂ = x̄</option><option value="shift">2θe^(−2θ(x−1)), x ≥ 1 → θ̂ = 1/(2(x̄−1)) (đề 2021–22)</option></select></label></div><div class="row"><label>Mẫu: <textarea id="d" rows="2">1.15 2.05 3.14 4.22 5.21 6.04</textarea></label></div><div class="out"></div>');
  var DEF={exp:'1.15 2.05 3.14 4.22 5.21 6.04',geo:'7 6',poi:'2 3 1 4 2 0 3',ber:'1 0 1 1 0 1 1 0',shift:'1.5 11.5 5.5 4 5 6'};
  function ll(m,xs,t){var n=xs.length,s=xs.reduce(function(a,b){return a+b},0),i;
    if(m==='exp')return n*Math.log(t)-t*s;
    if(m==='geo')return n*Math.log(t)+(s-n)*Math.log(1-t);
    if(m==='poi'){var l=-n*t+s*Math.log(t);return l}
    if(m==='ber')return s*Math.log(t)+(n-s)*Math.log(1-t);
    if(m==='shift')return n*Math.log(2)+n*Math.log(t)-2*t*(s-n)}
  function mle(m,xs){var n=xs.length,s=xs.reduce(function(a,b){return a+b},0),xb=s/n;
    if(m==='exp'||m==='geo')return n/s;if(m==='poi'||m==='ber')return xb;if(m==='shift')return 1/(2*(xb-1))}
  function run(){var m=$(root,'#m').value,out=$(root,'.out');try{var xs=nums($(root,'#d').value);if(!xs.length||xs.some(isNaN))throw new Error('Nhập các số hợp lệ.');
    if(m==='ber'&&xs.some(function(v){return v!==0&&v!==1}))throw new Error('Bernoulli chỉ nhận 0 hoặc 1.');if(m==='geo'&&xs.some(function(v){return v<1||v!==Math.floor(v)}))throw new Error('Hình học: số nguyên ≥ 1.');
    if(m==='shift'&&xs.some(function(v){return v<1}))throw new Error('Mô hình dịch chuyển cần mọi x ≥ 1.');if(m==='poi'&&xs.some(function(v){return v<0||v!==Math.floor(v)}))throw new Error('Poisson: số nguyên ≥ 0.');
    var t0=mle(m,xs),lo,hi;if(m==='geo'||m==='ber'){lo=0.005;hi=0.995}else{lo=Math.max(0.005,t0/4);hi=t0*3}
    var Wd=560,H=150,N=160,vals=[],mx=-Infinity,mn=Infinity;for(var i=0;i<=N;i++){var t=lo+(hi-lo)*i/N,v=ll(m,xs,t);vals.push([t,v]);mx=Math.max(mx,v);mn=Math.min(mn,v)}
    mn=Math.max(mn,mx-12);var X=function(t){return 40+(t-lo)/(hi-lo)*(Wd-60)},Y=function(v){return 10+(mx-Math.max(v,mn))/(mx-mn)*(H-20)},ac=SL.css('--accent2','#1f4e8c'),rd=SL.css('--accent','#b3122f'),tx=SL.css('--text','#222');
    var d=vals.map(function(q,i){return (i?'L':'M')+X(q[0]).toFixed(1)+' '+Y(q[1]).toFixed(1)}).join('');
    out.innerHTML='<svg viewBox="0 0 '+Wd+' '+(H+24)+'" style="max-width:100%;width:600px"><path d="'+d+'" fill="none" stroke="'+ac+'" stroke-width="2.5"/><line x1="'+X(t0)+'" y1="'+Y(ll(m,xs,t0))+'" x2="'+X(t0)+'" y2="'+H+'" stroke="'+rd+'" stroke-dasharray="4 3" stroke-width="2"/><circle cx="'+X(t0)+'" cy="'+Y(ll(m,xs,t0))+'" r="5" fill="'+rd+'"/><line x1="40" y1="'+H+'" x2="'+(Wd-20)+'" y2="'+H+'" stroke="'+tx+'"/><text x="'+(X(t0)+6)+'" y="22" font-size="12" fill="'+rd+'">θ̂ = '+F(t0,4)+'</text><text x="40" y="'+(H+16)+'" font-size="10" fill="'+tx+'">'+F(lo,3)+'</text><text x="'+(Wd-50)+'" y="'+(H+16)+'" font-size="10" fill="'+tx+'">'+F(hi,3)+'</text></svg><p>n = '+xs.length+' · Σx = '+F(xs.reduce(function(a,b){return a+b},0),4)+' · x̄ = '+F(xs.reduce(function(a,b){return a+b},0)/xs.length,4)+' · <b>ước lượng hợp lý cực đại = '+F(t0,5)+'</b> · ln l(θ̂) = '+F(ll(m,xs,t0),4)+'</p><p style="font-size:.8rem;color:var(--muted)">Đường cong là ln l(θ); đỉnh của nó là MLE. Dời mẫu để thấy đỉnh dịch chuyển.</p>'}catch(e){out.innerHTML='<p class="no">'+esc(e.message)+'</p>'}}
  $(root,'#m').onchange=function(){$(root,'#d').value=DEF[this.value];run()};$(root,'#d').oninput=run;run()};
W.samplemean=function(root){
  frame(root,'Phân phối của trung bình mẫu x̄ và phương sai mẫu s² (mô phỏng 2000 mẫu)',
   '<div class="row"><label>Tổng thể: <select id="p"><option value="n">chuẩn N(10, 4)</option><option value="u">đều trên [0, 20]</option><option value="e">mũ (trung bình 10)</option></select></label><label>Cỡ mẫu n: <input id="n" type="number" min="2" max="200" value="10" style="width:70px"></label><button class="btn" id="go">Mô phỏng lại</button></div><div class="out"></div>');
  function draw(){var kind=$(root,'#p').value,n=Math.max(2,Math.min(200,Math.round(+$(root,'#n').value||10))),R=2000,means=[],vs=[],vp=[],mu,vtrue;
    function gen(){if(kind==='n')return 10+2*rnorm();if(kind==='u')return 20*Math.random();return -10*Math.log(1-Math.random())}
    mu=kind==='n'?10:kind==='u'?10:10;vtrue=kind==='n'?4:kind==='u'?400/12:100;
    for(var r=0;r<R;r++){var xs=[],s=0;for(var i=0;i<n;i++){var v=gen();xs.push(v);s+=v}var m=s/n,ss=0;xs.forEach(function(v){ss+=(v-m)*(v-m)});means.push(m);vs.push(ss/(n-1));vp.push(ss/n)}
    var mm=PS.mean(means),sm=PS.sdS(means),mv=PS.mean(vs),mvp=PS.mean(vp);
    var lo=Math.min.apply(null,means),hi=Math.max.apply(null,means),k=30,w=(hi-lo)/k||1,c=[];for(var i=0;i<k;i++)c.push(0);means.forEach(function(v){c[Math.min(k-1,Math.floor((v-lo)/w))]++});
    var mx=Math.max.apply(null,c),Wd=560,H=130,bw=(Wd-50)/k,ac=SL.css('--accent2','#1f4e8c'),rd=SL.css('--accent','#b3122f'),tx=SL.css('--text','#222'),svg='<svg viewBox="0 0 '+Wd+' '+(H+24)+'" style="max-width:100%;width:600px">';
    c.forEach(function(v,i){var h=v/mx*(H-14);svg+='<rect x="'+(30+i*bw)+'" y="'+(H-h)+'" width="'+(bw-1)+'" height="'+h+'" fill="'+ac+'" opacity=".6"/>'});
    var xm=30+(mu-lo)/(hi-lo)*(Wd-50);svg+='<line x1="'+xm+'" y1="4" x2="'+xm+'" y2="'+H+'" stroke="'+rd+'" stroke-width="2" stroke-dasharray="4 3"/><line x1="30" y1="'+H+'" x2="'+(Wd-20)+'" y2="'+H+'" stroke="'+tx+'"/><text x="'+(xm+4)+'" y="14" font-size="11" fill="'+rd+'">μ = '+mu+'</text><text x="30" y="'+(H+14)+'" font-size="10" fill="'+tx+'">'+F(lo,2)+'</text><text x="'+(Wd-50)+'" y="'+(H+14)+'" font-size="10" fill="'+tx+'">'+F(hi,2)+'</text></svg>';
    $(root,'.out').innerHTML=svg+'<table class="t left"><tr><td>Trung bình của 2000 giá trị x̄</td><td><b>'+F(mm,4)+'</b> (μ = '+mu+') → không chệch</td></tr><tr><td>Độ lệch chuẩn của x̄ (mô phỏng)</td><td><b>'+F(sm,4)+'</b> · lý thuyết σ/√n = '+F(Math.sqrt(vtrue/n),4)+'</td></tr><tr><td>Trung bình của s² (chia n − 1)</td><td><b>'+F(mv,4)+'</b> (σ² = '+F(vtrue,3)+') → không chệch</td></tr><tr><td>Trung bình của σ̂² (chia n)</td><td><b>'+F(mvp,4)+'</b> → chệch xuống, ≈ (n−1)σ²/n = '+F((n-1)*vtrue/n,3)+'</td></tr></table><p style="font-size:.82rem;color:var(--muted)">Tăng n: biểu đồ x̄ hẹp lại (sai số chuẩn giảm theo √n) và gần dạng chuông dù tổng thể không chuẩn (định lý giới hạn trung tâm).</p>'}
  $(root,'#go').onclick=draw;$(root,'#p').onchange=draw;$(root,'#n').onchange=draw;draw()};
})();
