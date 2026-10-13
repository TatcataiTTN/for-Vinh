(function(){'use strict';
var SL=window.SL,PS=SL.PS,esc=SL.esc,frame=SL.frame,$=SL.$,nums=SL.nums,W=window.SIM_W;
function F(x,d){return PS.fmt(x,d===undefined?4:d)}
W.htest=function(root){
  frame(root,'Kiểm định giả thuyết về kỳ vọng: nhập số liệu → T_qs, miền bác bỏ, kết luận',
   '<div class="row"><label>Kiểu: <select id="k"><option value="t">σ chưa biết (Student)</option><option value="z">σ đã biết (U)</option></select></label><label>Đối thuyết H₁: <select id="alt"><option value=">">μ &gt; μ₀</option><option value="<">μ &lt; μ₀</option><option value="!">μ ≠ μ₀</option></select></label><label>α: <input id="al" type="number" step="any" value="0.05" style="width:70px"></label></div>'+
   '<div class="row"><label>μ₀ <input id="m0" type="number" step="any" value="5.75" style="width:80px"></label><label>x̄ <input id="xb" type="number" step="any" value="6.207" style="width:80px"></label><label><span id="sl">s</span> <input id="s" type="number" step="any" value="0.541" style="width:80px"></label><label>n <input id="n" type="number" value="27" style="width:70px"></label></div><div class="out"></div>');
  function run(){var t=$(root,'#k').value,alt=$(root,'#alt').value,al=+$(root,'#al').value,m0=+$(root,'#m0').value,xb=+$(root,'#xb').value,s=+$(root,'#s').value,n=Math.round(+$(root,'#n').value),out=$(root,'.out');
    $(root,'#sl').textContent=t==='z'?'σ':'s';if(!(al>0&&al<1)||!(s>0)||n<2){out.innerHTML='<p class="no">Kiểm tra α, s (σ) &gt; 0, n ≥ 2.</p>';return}
    var T=(xb-m0)/(s/Math.sqrt(n)),df=n-1,a=alt==='!'?al/2:al,crit=t==='z'?PS.uCrit(a):PS.tCrit(a,df),rej=alt==='>'?T>crit:alt==='<'?T<-crit:Math.abs(T)>crit;
    var pdf=function(x){return t==='z'?PS.normPdf(x):PS.tPdf(x,df)},lo=-5,hi=5,Wd=560,H=150,X=function(x){return 30+(x-lo)/(hi-lo)*(Wd-50)},Y=function(y){return H-y/0.43*(H-20)},ac=SL.css('--accent2','#1f4e8c'),rd=SL.css('--accent','#b3122f'),tx=SL.css('--text','#222'),d='',sh='';
    for(var i=0;i<=200;i++){var x=lo+10*i/200;d+=(i?'L':'M')+X(x).toFixed(1)+' '+Y(pdf(x)).toFixed(1)}
    function area(a0,b0){var p='M'+X(a0)+' '+Y(0);for(var i=0;i<=60;i++){var x=a0+(b0-a0)*i/60;p+='L'+X(x).toFixed(1)+' '+Y(pdf(x)).toFixed(1)}return p+'L'+X(b0)+' '+Y(0)+'Z'}
    if(alt==='>')sh=area(Math.min(crit,hi),hi);else if(alt==='<')sh=area(lo,Math.max(-crit,lo));else sh=area(Math.min(crit,hi),hi)+area(lo,Math.max(-crit,lo));
    var Tc=Math.max(lo,Math.min(hi,T));
    out.innerHTML='<svg viewBox="0 0 '+Wd+' '+(H+24)+'" style="max-width:100%;width:600px"><path d="'+sh+'" fill="'+rd+'" opacity=".35"/><path d="'+d+'" fill="none" stroke="'+ac+'" stroke-width="2.5"/><line x1="30" y1="'+Y(0)+'" x2="'+(Wd-20)+'" y2="'+Y(0)+'" stroke="'+tx+'"/><line x1="'+X(Tc)+'" y1="'+Y(0)+'" x2="'+X(Tc)+'" y2="14" stroke="'+(rej?rd:ac)+'" stroke-width="2.5"/><text x="'+(X(Tc)+4)+'" y="24" font-size="12" fill="'+(rej?rd:ac)+'">T_qs = '+F(T,3)+'</text></svg>'+
      '<table class="t left"><tr><td>H₀: μ = '+m0+' · H₁: μ '+(alt==='!'?'≠':alt)+' '+m0+'</td><td>mức ý nghĩa '+(al*100)+'%</td></tr><tr><td>T_qs = (x̄ − μ₀)/('+(t==='z'?'σ':'s')+'/√n)</td><td><b>'+F(T,4)+'</b></td></tr><tr><td>Giá trị tới hạn '+(t==='z'?'U':'t('+df+')')+(alt==='!'?'<sub>α/2</sub>':'<sub>α</sub>')+'</td><td><b>'+F(crit,4)+'</b></td></tr><tr><td>Miền bác bỏ W<sub>α</sub></td><td>'+(alt==='>'?'T &gt; '+F(crit,3):alt==='<'?'T &lt; −'+F(crit,3):'|T| &gt; '+F(crit,3))+' (vùng đỏ)</td></tr></table><div class="callout '+(rej?'bad':'good')+'"><b>Kết luận:</b> '+(rej?'T_qs ∈ W<sub>α</sub> ⇒ BÁC BỎ H₀, chấp nhận H₁.':'T_qs ∉ W<sub>α</sub> ⇒ chưa đủ cơ sở bác bỏ H₀ (chấp nhận H₀).')+'</div>'}
  root.querySelectorAll('input,select').forEach(function(i){i.oninput=run;i.onchange=run});run()};
})();
