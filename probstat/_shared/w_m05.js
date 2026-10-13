(function(){'use strict';
var SL=window.SL,PS=SL.PS,esc=SL.esc,frame=SL.frame,$=SL.$,nums=SL.nums,W=window.SIM_W;
function F(x,d){return PS.fmt(x,d===undefined?4:d)}
W.rv=function(root){
  frame(root,'Biến ngẫu nhiên rời rạc: bảng phân phối → kỳ vọng, phương sai, hàm phân phối F(x)',
   '<div class="row"><label>Giá trị xᵢ: <input id="x" value="0 1 2 3 4 5" size="18"></label><label>Xác suất pᵢ: <input id="p" value="0.10 0.20 0.25 0.35 0.06 0.04" size="30"></label><button class="btn" id="go">Tính</button></div><div class="out"></div>');
  function run(){var out=$(root,'.out');try{var x=nums($(root,'#x').value),p=nums($(root,'#p').value);if(x.length!==p.length||x.length<2||x.some(isNaN)||p.some(isNaN))throw new Error('Số giá trị và số xác suất phải bằng nhau (≥ 2).');
    var s=p.reduce(function(a,b){return a+b},0),idx=x.map(function(_,i){return i}).sort(function(a,b){return x[a]-x[b]}),xs=idx.map(function(i){return x[i]}),ps=idx.map(function(i){return p[i]});
    var warn=Math.abs(s-1)>1e-6?'<p class="no">Cảnh báo: Σpᵢ = '+F(s,6)+' ≠ 1. Không phải bảng phân phối hợp lệ.</p>':'<p class="ok">Σpᵢ = 1 ✓</p>';
    var m=0,e2=0;xs.forEach(function(v,i){m+=v*ps[i];e2+=v*v*ps[i]});var v=e2-m*m,cum=0,rows=xs.map(function(vv,i){cum+=ps[i];return [F(vv,4).replace(/\.?0+$/,''),F(ps[i],4),F(cum,4),F(vv*ps[i],4)]});
    var ac=SL.css('--accent2','#1f4e8c'),rd=SL.css('--accent','#b3122f'),tx=SL.css('--text','#222'),mx=Math.max.apply(null,ps),Wd=560,H=150,xmin=xs[0],xmax=xs[xs.length-1],span=(xmax-xmin)||1,X=function(t){return 40+(t-xmin)/span*(Wd-80)};
    var svg='<svg viewBox="0 0 '+Wd+' '+(H+40)+'" style="max-width:100%;width:600px"><line x1="30" y1="'+H+'" x2="'+(Wd-10)+'" y2="'+H+'" stroke="'+tx+'"/>';
    xs.forEach(function(vv,i){var h=ps[i]/mx*(H-30);svg+='<line x1="'+X(vv)+'" y1="'+H+'" x2="'+X(vv)+'" y2="'+(H-h)+'" stroke="'+ac+'" stroke-width="8" opacity=".6"/><text x="'+X(vv)+'" y="'+(H-h-4)+'" font-size="10" text-anchor="middle" fill="'+tx+'">'+F(ps[i],2)+'</text><text x="'+X(vv)+'" y="'+(H+14)+'" font-size="11" text-anchor="middle" fill="'+tx+'">'+vv+'</text>'});
    svg+='<line x1="'+X(m)+'" y1="'+(H+18)+'" x2="'+X(m)+'" y2="14" stroke="'+rd+'" stroke-dasharray="4 3" stroke-width="2"/><text x="'+(X(m)+4)+'" y="24" font-size="11" fill="'+rd+'">E(X) = '+F(m,3)+'</text></svg>';
    var cdf='<svg viewBox="0 0 '+Wd+' 130" style="max-width:100%;width:600px"><line x1="30" y1="110" x2="'+(Wd-10)+'" y2="110" stroke="'+tx+'"/>',c=0,prevX=X(xmin)-30;
    cdf+='<line x1="'+(X(xmin)-30)+'" y1="110" x2="'+X(xs[0])+'" y2="110" stroke="'+rd+'" stroke-width="2"/>';
    xs.forEach(function(vv,i){c+=ps[i];var y=110-c*95,x2=i<xs.length-1?X(xs[i+1]):X(vv)+30;cdf+='<line x1="'+X(vv)+'" y1="'+y+'" x2="'+x2+'" y2="'+y+'" stroke="'+rd+'" stroke-width="2"/><circle cx="'+X(vv)+'" cy="'+y+'" r="3" fill="'+rd+'"/>'});
    cdf+='<text x="34" y="14" font-size="11" fill="'+tx+'">F(x) = P(X ≤ x) — hàm bậc thang tăng từ 0 đến 1</text></svg>';
    out.innerHTML=warn+'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px"><div>'+SL.tbl(['x','p','F(x)','x·p'],rows)+'<p><b>E(X) = '+F(m)+'</b> · E(X²) = '+F(e2)+' · <b>Var(X) = '+F(v)+'</b> · σ = '+F(Math.sqrt(Math.max(v,0)))+'</p></div><div>'+svg+cdf+'</div></div>'}catch(e){out.innerHTML='<p class="no">'+esc(e.message)+'</p>'}}
  $(root,'#go').onclick=run;root.querySelectorAll('input').forEach(function(i){i.onchange=run});run()};
W.pdf=function(root){
  var T={'poly':['c·(L − x)·x trên [0, L] (dạng đề thi HK2)'],'pow':['c·xᵃ trên [0, L]'],'exp':['λ·e^(−λx), x ≥ 0 (mũ)'],'tri':['1 − |x| trên [−1, 1] (tam giác)']};
  frame(root,'Biến ngẫu nhiên liên tục: mật độ f(x), P(a < X < b) là diện tích, kỳ vọng, phương sai, trung vị',
   '<div class="row"><label>Dạng: <select id="t"><option value="poly">f(x) = c·(L − x)·x trên [0, L]</option><option value="pow">f(x) = c·xᵃ trên [0, L]</option><option value="exp">f(x) = λ·e^(−λx), x ≥ 0</option><option value="tri">f(x) = 1 − |x| trên [−1, 1]</option></select></label><label>L hoặc λ: <input id="L" type="number" step="any" value="1" style="width:70px"></label><label>a (số mũ): <input id="a" type="number" step="any" value="2" style="width:60px"></label></div><div class="row"><label>P(<input id="lo" type="number" step="any" value="0.2" style="width:70px"> &lt; X &lt; <input id="hi" type="number" step="any" value="0.7" style="width:70px">)</label></div><div class="out"></div>');
  function mk(){var t=$(root,'#t').value,L=+$(root,'#L').value,a=+$(root,'#a').value,fn,lo,hi;
    if(t==='poly'){lo=0;hi=L;var Z=L*L*L/6;fn=function(x){return x<0||x>L?0:(L-x)*x/Z}}
    else if(t==='pow'){lo=0;hi=L;fn=function(x){return x<0||x>L?0:(a+1)*Math.pow(x,a)/Math.pow(L,a+1)}}
    else if(t==='exp'){lo=0;hi=Math.min(8/L,60);fn=function(x){return x<0?0:L*Math.exp(-L*x)}}
    else{lo=-1;hi=1;fn=function(x){return Math.abs(x)>1?0:1-Math.abs(x)}}
    return {fn:fn,lo:lo,hi:hi,t:t}}
  function integ(fn,a,b){var n=2000,h=(b-a)/n,s=fn(a)+fn(b);for(var i=1;i<n;i++)s+=fn(a+i*h)*(i%2?4:2);return s*h/3}
  function run(){var d=mk(),out=$(root,'.out');if(!(+$(root,'#L').value>0)&&d.t!=='tri'){out.innerHTML='<p class="no">L (hoặc λ) phải dương.</p>';return}
    var tot=integ(d.fn,d.lo,d.hi),mu=integ(function(x){return x*d.fn(x)},d.lo,d.hi),e2=integ(function(x){return x*x*d.fn(x)},d.lo,d.hi),v=e2-mu*mu;
    var a=Math.max(d.lo,+$(root,'#lo').value),b=Math.min(d.hi,+$(root,'#hi').value),pr=b>a?integ(d.fn,a,b):0;
    var lo=d.lo,hi=d.hi,l=lo,h=hi;for(var i=0;i<80;i++){var m=(l+h)/2;if(integ(d.fn,lo,m)<0.5)l=m;else h=m}var med=(l+h)/2;
    var N=200,ymax=0;for(var i=0;i<=N;i++)ymax=Math.max(ymax,d.fn(lo+(hi-lo)*i/N));ymax*=1.1;var Wd=560,H=160,X=function(x){return 40+(x-lo)/(hi-lo)*(Wd-60)},Y=function(y){return H-y/ymax*(H-20)},ac=SL.css('--accent2','#1f4e8c'),rd=SL.css('--accent','#b3122f'),tx=SL.css('--text','#222');
    var path='',shade='M'+X(a)+' '+Y(0);for(var i=0;i<=N;i++){var x=lo+(hi-lo)*i/N;path+=(i?'L':'M')+X(x).toFixed(1)+' '+Y(d.fn(x)).toFixed(1)}
    for(var i=0;i<=N;i++){var x=a+(b-a)*i/N;if(b>a)shade+='L'+X(x).toFixed(1)+' '+Y(d.fn(x)).toFixed(1)}shade+='L'+X(b)+' '+Y(0)+'Z';
    out.innerHTML='<svg viewBox="0 0 '+Wd+' '+(H+30)+'" style="max-width:100%;width:600px"><path d="'+shade+'" fill="'+rd+'" opacity=".3"/><path d="'+path+'" fill="none" stroke="'+ac+'" stroke-width="2.5"/><line x1="30" y1="'+Y(0)+'" x2="'+(Wd-10)+'" y2="'+Y(0)+'" stroke="'+tx+'"/><line x1="'+X(mu)+'" y1="'+Y(0)+'" x2="'+X(mu)+'" y2="14" stroke="'+rd+'" stroke-dasharray="4 3" stroke-width="2"/><text x="'+(X(mu)+4)+'" y="24" font-size="11" fill="'+rd+'">μ = '+F(mu,3)+'</text><text x="30" y="'+(H+16)+'" font-size="10" fill="'+tx+'">'+F(lo,2)+'</text><text x="'+(Wd-40)+'" y="'+(H+16)+'" font-size="10" fill="'+tx+'">'+F(hi,2)+'</text></svg>'+
      '<table class="t left"><tr><td>∫f(x)dx (phải = 1)</td><td><b>'+F(tot,5)+'</b></td></tr><tr><td>Kỳ vọng E(X)</td><td><b>'+F(mu)+'</b></td></tr><tr><td>Phương sai Var(X)</td><td><b>'+F(v)+'</b> (σ = '+F(Math.sqrt(v))+')</td></tr><tr><td>Trung vị m: F(m) = 0.5</td><td><b>'+F(med)+'</b></td></tr><tr><td>P('+F(a,3)+' &lt; X &lt; '+F(b,3)+') (vùng tô)</td><td><b>'+F(pr,5)+'</b></td></tr></table>'}
  root.querySelectorAll('input,select').forEach(function(i){i.onchange=run;i.oninput=run});run()};
})();
