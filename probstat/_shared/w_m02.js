(function(){'use strict';
var SL=window.SL,PS=SL.PS,esc=SL.esc,frame=SL.frame,$=SL.$,W=window.SIM_W;
function fact(n){var r=1n;for(var i=2n;i<=BigInt(n);i++)r*=i;return r}
function permB(n,k){var r=1n;for(var i=0n;i<BigInt(k);i++)r*=BigInt(n)-i;return r}
function combB(n,k){if(k<0||k>n)return 0n;var r=1n;k=Math.min(k,n-k);for(var i=1n;i<=BigInt(k);i++)r=r*(BigInt(n)-BigInt(k)+i)/i;return r}
function G(x){return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g,' ')}
W.count=function(root){
  frame(root,'Máy tính đếm: hoán vị, chỉnh hợp, tổ hợp (số lớn dùng BigInt, chính xác tuyệt đối)',
   '<div class="row"><label>n = <input id="n" type="number" min="0" max="200" value="10" style="width:80px"></label><label>k = <input id="k" type="number" min="0" max="200" value="3" style="width:80px"></label></div><div class="out"></div>'+
   '<div class="row"><label>Hoán vị có lặp: các số lần lặp n₁, n₂, … = <input id="m" value="2 3 2" size="14"> → <b id="mp"></b></label></div>');
  function run(){var n=Math.max(0,Math.min(200,Math.round(+$(root,'#n').value))),k=Math.max(0,Math.min(200,Math.round(+$(root,'#k').value)));
    var rows=[['n! (hoán vị n phần tử khác nhau)',G(fact(n))]];
    if(k<=n){rows.push(['A(n,k) = n!/(n−k)! (chỉnh hợp không lặp)',G(permB(n,k))]);rows.push(['C(n,k) = n!/(k!(n−k)!) (tổ hợp)',G(combB(n,k))])}
    else rows.push(['A(n,k), C(n,k)','không xác định vì k > n']);
    rows.push(['nᵏ (chỉnh hợp lặp)',G(BigInt(n)**BigInt(k))]);rows.push(['C(n+k−1,k) (tổ hợp lặp)',G(combB(n+k-1,k))]);
    $(root,'.out').innerHTML='<table class="t left">'+rows.map(function(r){return '<tr><td>'+r[0]+'</td><td><b>'+r[1]+'</b></td></tr>'}).join('')+'</table>';
    var ms=$(root,'#m').value.split(/[\s,;]+/).filter(Boolean).map(Number),tot=ms.reduce(function(a,b){return a+b},0),den=1n;ms.forEach(function(v){den*=fact(v)});
    $(root,'#mp').textContent=ms.length&&ms.every(function(v){return v>=0&&Number.isInteger(v)})&&tot<=200?(tot+'!/('+ms.map(function(v){return v+'!'}).join('·')+') = '+G(fact(tot)/den)):'—'}
  root.querySelectorAll('input').forEach(function(i){i.oninput=run});run()};
W.dice=function(root){
  var EV={'eq':['hai mặt bằng nhau',function(a,b){return a===b}],'s7':['tổng = 7',function(a,b){return a+b===7}],'s9':['tổng > 9',function(a,b){return a+b>9}],'lt5':['tổng < 5',function(a,b){return a+b<5}],'even':['tổng là số chẵn',function(a,b){return (a+b)%2===0}],'d3':['tổng chia hết cho 3',function(a,b){return (a+b)%3===0}],'d5':['tổng chia hết cho 5',function(a,b){return (a+b)%5===0}],'a1':['súc sắc thứ nhất ra 1',function(a,b){return a===1}],'b6':['súc sắc thứ hai ra 6',function(a,b){return b===6}]};
  var opts=Object.keys(EV).map(function(k){return '<option value="'+k+'">'+EV[k][0]+'</option>'}).join('');
  frame(root,'Gieo hai súc sắc: không gian mẫu 36 điểm, biến cố A, B, A∩B, A∪B',
   '<div class="row"><label>A: <select id="a">'+opts+'</select></label><label>B: <select id="b">'+opts.replace('value="eq"','value="eq"').replace('<option value="s9">','<option value="s9" selected>')+'</select></label></div><div class="out"></div>');
  $(root,'#a').value='eq';$(root,'#b').value='lt5';
  function run(){var fa=EV[$(root,'#a').value][1],fb=EV[$(root,'#b').value][1],cA=0,cB=0,cI=0,html='<table class="t" style="border-spacing:0"><tr><th>1\\2</th>'+[1,2,3,4,5,6].map(function(j){return '<th>'+j+'</th>'}).join('')+'</tr>';
    for(var i=1;i<=6;i++){html+='<tr><th>'+i+'</th>';for(var j=1;j<=6;j++){var a=fa(i,j),b=fb(i,j);if(a)cA++;if(b)cB++;if(a&&b)cI++;
      var bg=a&&b?'background:#f6c445':a?'background:#9ec5fe':b?'background:#a3e4b1':'';html+='<td style="'+bg+';color:#111;min-width:30px">'+(a||b?'●':'')+'</td>'}html+='</tr>'}
    html+='</table><p style="font-size:.85rem">Xanh dương: chỉ A · Xanh lá: chỉ B · Vàng: cả A và B (A∩B). Mỗi ô là kết cục (a, b).</p>';
    var un=cA+cB-cI;html+='<table class="t"><tr><th>|A|</th><th>|B|</th><th>|A∩B|</th><th>|A∪B|</th><th>|Aᶜ|</th><th>P(A)</th><th>P(B)</th><th>P(A∪B)</th><th>Xung khắc?</th></tr><tr><td>'+cA+'</td><td>'+cB+'</td><td>'+cI+'</td><td>'+un+'</td><td>'+(36-cA)+'</td><td>'+(cA/36).toFixed(4)+'</td><td>'+(cB/36).toFixed(4)+'</td><td>'+(un/36).toFixed(4)+'</td><td>'+(cI===0?'<span class="ok">Có</span>':'<span class="no">Không</span>')+'</td></tr></table>';
    $(root,'.out').innerHTML=html}
  $(root,'#a').onchange=run;$(root,'#b').onchange=run;run()};
})();
