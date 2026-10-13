(function(){'use strict';
var SL=window.SL,PS=SL.PS,esc=SL.esc,frame=SL.frame,$=SL.$,W=window.SIM_W;
function F(x,d){return PS.fmt(x,d===undefined?4:d)}
W.normcalc=function(root){
  frame(root,'Máy tính phân phối chuẩn: xác suất, phân vị, vùng tô',
   '<div class="row"><label>μ = <input id="mu" type="number" step="any" value="12.5" style="width:80px"></label><label>σ = <input id="sg" type="number" step="any" value="0.809" style="width:80px"></label></div>'+
   '<div class="row"><label>Xác suất: P(<input id="a" type="number" step="any" value="11" style="width:80px"> &lt; X &lt; <input id="b" type="number" step="any" value="13.7135" style="width:90px">)</label><span style="font-size:.8rem;color:var(--muted)">(để trống/−∞ bằng −999; +∞ bằng 999)</span></div>'+
   '<div class="row"><label>Phân vị: P(X ≤ c) = <input id="p" type="number" step="any" value="0.99" style="width:80px"> → c = <b id="c"></b></label></div><div class="out"></div>');
  function run(){var mu=+$(root,'#mu').value,sg=+$(root,'#sg').value,a=+$(root,'#a').value,b=+$(root,'#b').value,p=+$(root,'#p').value,out=$(root,'.out');
    if(!(sg>0)){out.innerHTML='<p class="no">σ phải dương.</p>';return}
    var za=a<=-999?-Infinity:(a-mu)/sg,zb=b>=999?Infinity:(b-mu)/sg,pr=PS.normCdf(zb)-PS.normCdf(za);$(root,'#c').textContent=(p>0&&p<1)?F(mu+sg*PS.normInv(p),4)+'  (z = '+F(PS.normInv(p),4)+')':'—';
    var lo=mu-4*sg,hi=mu+4*sg,Wd=560,H=150,X=function(x){return 30+(x-lo)/(hi-lo)*(Wd-50)},Y=function(z){return H-PS.normPdf(z)/0.42*(H-20)},ac=SL.css('--accent2','#1f4e8c'),rd=SL.css('--accent','#b3122f'),tx=SL.css('--text','#222'),d='',sh='';
    for(var i=0;i<=200;i++){var x=lo+(hi-lo)*i/200,z=(x-mu)/sg;d+=(i?'L':'M')+X(x).toFixed(1)+' '+Y(z).toFixed(1)}
    var A=Math.max(lo,Math.min(hi,a<=-999?lo:a)),Bv=Math.min(hi,Math.max(lo,b>=999?hi:b));if(Bv>A){sh='M'+X(A)+' '+Y(-9);for(var i=0;i<=100;i++){var x=A+(Bv-A)*i/100;sh+='L'+X(x).toFixed(1)+' '+Y((x-mu)/sg).toFixed(1)}sh+='L'+X(Bv)+' '+Y(-9)+'Z'}
    out.innerHTML='<svg viewBox="0 0 '+Wd+' '+(H+24)+'" style="max-width:100%;width:600px"><path d="'+sh+'" fill="'+rd+'" opacity=".3"/><path d="'+d+'" fill="none" stroke="'+ac+'" stroke-width="2.5"/><line x1="30" y1="'+Y(-9)+'" x2="'+(Wd-20)+'" y2="'+Y(-9)+'" stroke="'+tx+'"/><line x1="'+X(mu)+'" y1="'+Y(-9)+'" x2="'+X(mu)+'" y2="'+Y(0)+'" stroke="'+tx+'" stroke-dasharray="3 3"/><text x="'+X(mu)+'" y="'+(H+14)+'" font-size="10" text-anchor="middle" fill="'+tx+'">μ='+mu+'</text></svg><table class="t left"><tr><td>z₁ = (a − μ)/σ</td><td><b>'+F(za,4)+'</b></td></tr><tr><td>z₂ = (b − μ)/σ</td><td><b>'+F(zb,4)+'</b></td></tr><tr><td>P(a &lt; X &lt; b) = Φ(z₂) − Φ(z₁) (vùng tô)</td><td><b>'+F(pr,5)+'</b></td></tr></table>'}
  root.querySelectorAll('input').forEach(function(i){i.oninput=run});run()};
W.binpois=function(root){
  frame(root,'Nhị thức B(n, p) so với Poisson(np) và chuẩn N(np, np(1−p))',
   '<div class="row"><label>n = <input id="n" type="number" min="1" max="500" value="100" style="width:70px"></label><label>p = <input id="p" type="number" step="any" min="0.0001" max="0.9999" value="0.04" style="width:80px"></label></div><div class="out"></div>');
  function run(){var n=Math.max(1,Math.min(500,Math.round(+$(root,'#n').value))),p=+$(root,'#p').value,out=$(root,'.out');if(!(p>0&&p<1)){out.innerHTML='<p class="no">0 &lt; p &lt; 1.</p>';return}
    var mu=n*p,sg=Math.sqrt(n*p*(1-p)),lo=Math.max(0,Math.floor(mu-4*sg)),hi=Math.min(n,Math.ceil(mu+4*sg)),Wd=560,H=150,mx=0,ac=SL.css('--accent2','#1f4e8c'),rd=SL.css('--accent','#b3122f'),gr=SL.css('--good','#1b7f4c'),tx=SL.css('--text','#222'),pts=[];
    for(var k=lo;k<=hi;k++){var b=PS.binomPmf(k,n,p),po=PS.poisPmf(k,mu),no=PS.normCdf((k+0.5-mu)/sg)-PS.normCdf((k-0.5-mu)/sg);mx=Math.max(mx,b,po,no);pts.push([k,b,po,no])}
    var X=function(k){return 30+(k-lo+0.5)/(hi-lo+1)*(Wd-50)},Y=function(v){return H-v/mx*(H-20)},bw=(Wd-50)/(hi-lo+1)*0.8,svg='<svg viewBox="0 0 '+Wd+' '+(H+26)+'" style="max-width:100%;width:620px">';
    pts.forEach(function(q){svg+='<rect x="'+(X(q[0])-bw/2)+'" y="'+Y(q[1])+'" width="'+bw+'" height="'+(H-Y(q[1]))+'" fill="'+ac+'" opacity=".45"/>'});
    svg+='<path d="'+pts.map(function(q,i){return (i?'L':'M')+X(q[0]).toFixed(1)+' '+Y(q[2]).toFixed(1)}).join('')+'" fill="none" stroke="'+rd+'" stroke-width="2"/><path d="'+pts.map(function(q,i){return (i?'L':'M')+X(q[0]).toFixed(1)+' '+Y(q[3]).toFixed(1)}).join('')+'" fill="none" stroke="'+gr+'" stroke-width="2" stroke-dasharray="5 3"/><line x1="30" y1="'+H+'" x2="'+(Wd-20)+'" y2="'+H+'" stroke="'+tx+'"/>';
    for(var k=lo;k<=hi;k+=Math.max(1,Math.round((hi-lo)/10)))svg+='<text x="'+X(k)+'" y="'+(H+14)+'" font-size="10" text-anchor="middle" fill="'+tx+'">'+k+'</text>';
    svg+='</svg><div style="font-size:.8rem">Cột xanh: nhị thức · Đường đỏ liền: Poisson · Đường xanh lá nét đứt: chuẩn (hiệu chỉnh 0.5)</div>';
    var kx=Math.round(mu),rows=[['P(X ≤ '+kx+') nhị thức',F(PS.binomCdf(kx,n,p))],['P(X ≤ '+kx+') Poisson(np)',F(PS.poisCdf(kx,mu))],['P(X ≤ '+kx+') chuẩn có hiệu chỉnh',F(PS.normCdf((kx+0.5-mu)/sg))]];
    out.innerHTML=svg+'<p>μ = np = <b>'+F(mu,3)+'</b>, σ² = np(1−p) = <b>'+F(sg*sg,3)+'</b>. Điều kiện chuẩn: np '+(mu>5?'> 5 ✓':'≤ 5 ✗')+', n(1−p) '+(n*(1-p)>5?'> 5 ✓':'≤ 5 ✗')+'. Poisson tốt khi p nhỏ: p = '+p+(p<0.05?' ✓':' (khá lớn)')+'.</p><table class="t left">'+rows.map(function(r){return '<tr><td>'+r[0]+'</td><td><b>'+r[1]+'</b></td></tr>'}).join('')+'</table>'}
  root.querySelectorAll('input').forEach(function(i){i.oninput=run});run()};
})();
