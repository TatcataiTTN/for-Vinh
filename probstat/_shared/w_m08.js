(function(){'use strict';
var SL=window.SL,PS=SL.PS,esc=SL.esc,frame=SL.frame,$=SL.$,nums=SL.nums,W=window.SIM_W;
function F(x,d){return PS.fmt(x,d===undefined?4:d)}
function rnorm(){var u=0,v=0;while(!u)u=Math.random();while(!v)v=Math.random();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v)}
W.cicalc=function(root){
  frame(root,'Máy tính khoảng tin cậy: μ (σ biết), μ (σ chưa biết), tỷ lệ p, cỡ mẫu',
   '<div class="row"><label>Loại: <select id="k"><option value="z">μ, σ đã biết (U)</option><option value="t">μ, σ chưa biết (Student)</option><option value="p">tỷ lệ p</option><option value="n">cỡ mẫu cho độ dài L (σ biết)</option></select></label><label>Độ tin cậy γ: <input id="g" type="number" step="any" value="0.95" style="width:70px"></label></div>'+
   '<div class="row" id="f1"></div><div class="out"></div>');
  var cur='z';
  function fields(){var k=$(root,'#k').value;cur=k;var h='';
    if(k==='z')h='<label>x̄ <input id="a" type="number" step="any" value="115.278" style="width:90px"></label><label>σ <input id="b" type="number" step="any" value="16" style="width:70px"></label><label>n <input id="c" type="number" value="27" style="width:70px"></label>';
    if(k==='t')h='<label>x̄ <input id="a" type="number" step="any" value="174.5" style="width:90px"></label><label>s <input id="b" type="number" step="any" value="2.4" style="width:70px"></label><label>n <input id="c" type="number" value="22" style="width:70px"></label>';
    if(k==='p')h='<label>số thành công <input id="a" type="number" value="960" style="width:90px"></label><label>n <input id="c" type="number" value="1600" style="width:80px"></label>';
    if(k==='n')h='<label>σ <input id="b" type="number" step="any" value="3" style="width:70px"></label><label>độ dài L <input id="a" type="number" step="any" value="0.4" style="width:70px"></label>';
    $(root,'#f1').innerHTML=h;root.querySelectorAll('#f1 input').forEach(function(i){i.oninput=run});run()}
  function run(){var g=+$(root,'#g').value,out=$(root,'.out');if(!(g>0&&g<1)){out.innerHTML='<p class="no">Độ tin cậy γ ∈ (0, 1).</p>';return}
    var al=1-g,a=+($(root,'#a')||{}).value,b=+($(root,'#b')||{}).value,n=Math.round(+($(root,'#c')||{}).value),k=cur,z=PS.uCrit(al/2),h='';
    if(k==='z'){var kk=z*b/Math.sqrt(n);h='U<sub>α/2</sub> = '+F(z,4)+'; k = U·σ/√n = '+F(kk,4)+'<br><b>μ ∈ ['+F(a-kk,3)+'; '+F(a+kk,3)+']</b>'}
    if(k==='t'){var t=PS.tCrit(al/2,n-1),kk=t*b/Math.sqrt(n);h='t<sub>α/2</sub>('+(n-1)+') = '+F(t,4)+'; k = t·s/√n = '+F(kk,4)+'<br><b>μ ∈ ['+F(a-kk,3)+'; '+F(a+kk,3)+']</b> (so với dùng U: k = '+F(z*b/Math.sqrt(n),4)+')'}
    if(k==='p'){var fq=a/n,kk=z*Math.sqrt(fq*(1-fq)/n);h='f = '+F(fq,4)+'; U<sub>α/2</sub> = '+F(z,4)+'; k = U·√(f(1−f)/n) = '+F(kk,4)+'<br><b>p ∈ ['+F(fq-kk,4)+'; '+F(fq+kk,4)+']</b>'}
    if(k==='n'){var nn=Math.pow(2*z*b/a,2);h='n ≥ (2·U·σ/L)² = '+F(nn,2)+'<br><b>n nhỏ nhất = '+Math.ceil(nn)+'</b>'}
    out.innerHTML='<div class="callout good">'+h+'</div>'}
  $(root,'#k').onchange=fields;$(root,'#g').oninput=run;fields()};
W.ciplay=function(root){
  frame(root,'Ý nghĩa “độ tin cậy 95%”: dựng nhiều khoảng từ nhiều mẫu',
   '<div class="row"><label>γ: <select id="g"><option value="0.8">80%</option><option value="0.9">90%</option><option value="0.95" selected>95%</option><option value="0.99">99%</option></select></label><label>cỡ mẫu n: <input id="n" type="number" min="2" max="200" value="10" style="width:70px"></label><label>Dùng: <select id="m"><option value="z">σ biết (U)</option><option value="t">σ chưa biết (t)</option></select></label><button class="btn" id="go">Lấy 60 mẫu mới</button></div><div class="out"></div>');
  function run(){var g=+$(root,'#g').value,n=Math.max(2,Math.min(200,Math.round(+$(root,'#n').value||10))),m=$(root,'#m').value,R=60,mu=0,sg=1,al=1-g,cover=0,Wd=560,H=R*6+16,rows='',lo=-1.4,hi=1.4,X=function(x){return 30+(x-lo)/(hi-lo)*(Wd-50)},rd=SL.css('--bad','#b3122f'),ac=SL.css('--accent2','#1f4e8c'),tx=SL.css('--text','#222');
    for(var r=0;r<R;r++){var xs=[],s=0;for(var i=0;i<n;i++){var v=mu+sg*rnorm();xs.push(v);s+=v}var xb=s/n,ss=0;xs.forEach(function(v){ss+=(v-xb)*(v-xb)});var sd=Math.sqrt(ss/(n-1)),k=(m==='z'?PS.uCrit(al/2)*sg:PS.tCrit(al/2,n-1)*sd)/Math.sqrt(n),ok=xb-k<=mu&&mu<=xb+k;if(ok)cover++;
      var y=8+r*6;rows+='<line x1="'+X(xb-k)+'" y1="'+y+'" x2="'+X(xb+k)+'" y2="'+y+'" stroke="'+(ok?ac:rd)+'" stroke-width="2.4"/><circle cx="'+X(xb)+'" cy="'+y+'" r="1.8" fill="'+(ok?ac:rd)+'"/>'}
    $(root,'.out').innerHTML='<svg viewBox="0 0 '+Wd+' '+H+'" style="max-width:100%;width:600px">'+rows+'<line x1="'+X(0)+'" y1="0" x2="'+X(0)+'" y2="'+H+'" stroke="'+tx+'" stroke-dasharray="4 3"/><text x="'+(X(0)+4)+'" y="'+(H-3)+'" font-size="10" fill="'+tx+'">μ = 0 (thật)</text></svg><p>Có <b>'+cover+'/'+R+'</b> khoảng chứa μ ('+(cover/R*100).toFixed(0)+'%); kỳ vọng ≈ '+(g*100)+'%. Khoảng đỏ là khoảng “trượt” μ. Tham số μ cố định; khoảng mới ngẫu nhiên.</p>'}
  $(root,'#go').onclick=run;$(root,'#g').onchange=run;$(root,'#n').onchange=run;$(root,'#m').onchange=run;run()};
})();
