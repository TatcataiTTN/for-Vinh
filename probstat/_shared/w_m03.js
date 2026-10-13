(function(){'use strict';
var SL=window.SL,PS=SL.PS,esc=SL.esc,frame=SL.frame,$=SL.$,W=window.SIM_W;
W.cond=function(root){
  frame(root,'Bảng 2×2: xác suất, xác suất có điều kiện và kiểm tra độc lập',
   '<div class="row"><label>A∩B: <input id="a" type="number" min="0" value="30" style="width:70px"></label><label>A, không B: <input id="b" type="number" min="0" value="20" style="width:70px"></label><label>B, không A: <input id="c" type="number" min="0" value="15" style="width:70px"></label><label>không A, không B: <input id="d" type="number" min="0" value="35" style="width:70px"></label></div><div class="out"></div>');
  function run(){var v=['a','b','c','d'].map(function(k){return Math.max(0,+$(root,'#'+k).value||0)}),a=v[0],b=v[1],c=v[2],d=v[3],n=a+b+c+d;
    if(!n){$(root,'.out').innerHTML='<p class="no">Nhập ít nhất một số dương.</p>';return}
    var pa=(a+b)/n,pb=(a+c)/n,pab=a/n,F=function(x){return x.toFixed(4)},ind=Math.abs(pab-pa*pb)<1e-9;
    var rows=[['P(A)','(a+b)/n',F(pa)],['P(B)','(a+c)/n',F(pb)],['P(A∩B)','a/n',F(pab)],['P(A∪B)','P(A)+P(B)−P(A∩B)',F(pa+pb-pab)],['P(A|B)','P(A∩B)/P(B)',pb>0?F(pab/pb):'—'],['P(B|A)','P(A∩B)/P(A)',pa>0?F(pab/pa):'—'],['P(A)·P(B)','tích nếu độc lập',F(pa*pb)],['P(Aᶜ∩Bᶜ)','d/n',F(d/n)]];
    $(root,'.out').innerHTML='<table class="t"><tr><th></th><th>B</th><th>không B</th><th>Tổng</th></tr><tr><th>A</th><td>'+a+'</td><td>'+b+'</td><td>'+(a+b)+'</td></tr><tr><th>không A</th><td>'+c+'</td><td>'+d+'</td><td>'+(c+d)+'</td></tr><tr><th>Tổng</th><td>'+(a+c)+'</td><td>'+(b+d)+'</td><td>'+n+'</td></tr></table>'+
      '<table class="t left">'+rows.map(function(r){return '<tr><td><b>'+r[0]+'</b></td><td>'+r[1]+'</td><td>'+r[2]+'</td></tr>'}).join('')+'</table><p>'+(ind?'<span class="ok">P(A∩B) = P(A)P(B): A và B độc lập.</span>':'<span class="no">P(A∩B) ≠ P(A)P(B): A và B không độc lập (P(A|B) '+(pb>0?(pab/pb>pa?'>':'<'):'')+' P(A)).</span>')+'</p>'}
  root.querySelectorAll('input').forEach(function(i){i.oninput=run});run()};
W.lln=function(root){
  frame(root,'Luật số lớn: tần suất tương đối tiến về xác suất',
   '<div class="row"><label>Thực nghiệm: <select id="e"><option value="0.5">tung đồng xu: ngửa (p = 1/2)</option><option value="0.1667">gieo súc sắc: ra mặt 6 (p = 1/6)</option><option value="0.5833">gieo 2 súc sắc: tổng ≥ 6? (p = 26/36… xem dưới)</option><option value="0.3">sự kiện tuỳ ý p = 0.3</option></select></label><label>Số phép thử: <input id="n" type="number" min="10" max="200000" value="2000" style="width:90px"></label><button class="btn" id="go">Mô phỏng lại</button></div><div class="out"></div>');
  var sel=$(root,'#e');sel.options[2].textContent='gieo 2 súc sắc: tổng ≥ 8 (p = 15/36)';sel.options[2].value=String(15/36);
  function run(){var p=+sel.value,n=Math.max(10,Math.min(200000,+$(root,'#n').value||1000)),s=0,pts=[],step=Math.max(1,Math.floor(n/200));
    for(var i=1;i<=n;i++){if(Math.random()<p)s++;if(i%step===0||i===n)pts.push([i,s/i])}
    var Wd=560,H=170,X=function(i){return 40+i/n*(Wd-50)},Y=function(v){return 10+(1-v)*(H-20)},tx=SL.css('--text','#222'),ac=SL.css('--accent2','#1f4e8c'),rd=SL.css('--accent','#b3122f');
    var d=pts.map(function(q,i){return (i?'L':'M')+X(q[0]).toFixed(1)+' '+Y(q[1]).toFixed(1)}).join(' ');
    $(root,'.out').innerHTML='<svg viewBox="0 0 '+Wd+' '+(H+20)+'" style="max-width:100%;width:600px"><line x1="40" y1="'+Y(0)+'" x2="'+(Wd-10)+'" y2="'+Y(0)+'" stroke="'+tx+'"/><line x1="40" y1="10" x2="40" y2="'+Y(0)+'" stroke="'+tx+'"/><line x1="40" y1="'+Y(p)+'" x2="'+(Wd-10)+'" y2="'+Y(p)+'" stroke="'+rd+'" stroke-dasharray="5 4"/><path d="'+d+'" fill="none" stroke="'+ac+'" stroke-width="2"/><text x="42" y="'+(Y(p)-4)+'" font-size="11" fill="'+rd+'">P = '+p.toFixed(4)+'</text><text x="40" y="'+(H+16)+'" font-size="10" fill="'+tx+'">0</text><text x="'+(Wd-30)+'" y="'+(H+16)+'" font-size="10" fill="'+tx+'">'+n+'</text></svg><p>Sau '+n+' phép thử: tần suất = <b>'+(s/n).toFixed(4)+'</b> (xác suất thật '+p.toFixed(4)+'); sai lệch '+Math.abs(s/n-p).toFixed(4)+' ≈ cỡ 1/√n = '+(1/Math.sqrt(n)).toFixed(4)+'.</p>'}
  $(root,'#go').onclick=run;sel.onchange=run;$(root,'#n').onchange=run;run()};
})();
