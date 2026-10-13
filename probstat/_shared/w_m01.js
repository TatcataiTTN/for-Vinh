(function(){'use strict';
var SL=window.SL,PS=SL.PS,esc=SL.esc,frame=SL.frame,$=SL.$,nums=SL.nums,F=SL.F,tbl=SL.tbl,css=SL.css,W=window.SIM_W;

/* ---------- M1: thống kê mô tả + histogram + boxplot + stem-and-leaf ---------- */
W.descr=function(root){
  frame(root,'Thống kê mô tả: nhập dữ liệu, xem trung bình, phương sai, tứ phân vị, boxplot, histogram','<div class="row"><label>Dữ liệu (cách nhau bởi dấu cách/phẩy): <textarea id="d" rows="2">78 81 83 84 86 87 87 89 89 89 89 90 91 99</textarea></label></div>'+
    '<div class="row"><label>Số lớp histogram: <input id="k" type="number" min="2" max="15" value="5" style="width:60px"></label><button class="btn" id="go">Tính</button><select id="pre"><option value="">— chọn bộ dữ liệu mẫu —</option><option value="78 81 83 84 86 87 87 89 89 89 89 90 91 99">Sức căng thép (giáo trình ví dụ 1.1)</option><option value="156 158 154 133 141 130 144 137 151 146 156 138 138 149 139">Huyết áp 15 bệnh nhân (Kreyszig 24.1/3)</option><option value="86 86 87 89 76 85 82 86 87 85 90 88 89 90 88 80 84 89 90 89">Độ cứng Brinell (Kreyszig 24.1/8)</option><option value="1.3 1.2 1.4 1.5 1.3 1.3 1.4 1.1 1.5 1.4 1.6 1.3 1.5 1.1 1.4 1.2 1.3 1.5 1.4 1.4">Thời gian nhả rơ-le (Kreyszig 24.1/7)</option><option value="4 1 3 10 2">Có ngoại lai (Kreyszig 24.1/17)</option></select></div><div class="out"></div>');
  function run(){var out=$(root,'.out');
    try{var x=nums($(root,'#d').value);if(x.length<2||x.some(isNaN))throw new Error('Cần ít nhất 2 số hợp lệ.');
      var n=x.length,m=PS.mean(x),q=PS.quartiles(x),R=q.qU-q.qL,ol=PS.outliers(x),s=PS.sdS(x),sorted=PS.sorted(x);
      var lo=q.qL-1.5*R,hi=q.qU+1.5*R,mn=sorted[0],mx=sorted[n-1];
      var rows=[['n',n],['Σx',F(x.reduce(function(a,b){return a+b},0),4)],['Trung bình x̄',F(m)],['Trung vị qM',F(q.qM)],['qL (tứ vị 1)',F(q.qL)],['qU (tứ vị 3)',F(q.qU)],['IQR = qU − qL',F(R)],['Ngưỡng ngoại lai',F(lo)+' … '+F(hi)],['Ngoại lai',ol.length?ol.join(', '):'không có'],['Phương sai s² (n−1)',F(PS.varS(x))],['Độ lệch chuẩn s',F(s)],['Phương sai tổng thể (chia n)',F(PS.varP(x))],['Độ rộng R',F(mx-mn)]];
      var k=Math.max(2,Math.min(15,+$(root,'#k').value||5)),w=(mx-mn)/k||1,cnt=[];for(var i=0;i<k;i++)cnt.push(0);x.forEach(function(v){var j=Math.min(k-1,Math.floor((v-mn)/w));cnt[j]++});
      var mxc=Math.max.apply(null,cnt),W0=520,H0=170,bw=W0/k;var acc=css('--accent2','#1f4e8c'),tx=css('--text','#222'),mu=css('--muted','#666');
      var hist='<svg viewBox="0 0 '+(W0+40)+' '+(H0+40)+'" style="max-width:100%;width:560px"><g transform="translate(30,10)">';
      cnt.forEach(function(c,i){var h=c/mxc*(H0-20);hist+='<rect x="'+(i*bw+1)+'" y="'+(H0-h)+'" width="'+(bw-2)+'" height="'+h+'" fill="'+acc+'" opacity=".75"/><text x="'+(i*bw+bw/2)+'" y="'+(H0-h-3)+'" font-size="11" fill="'+tx+'" text-anchor="middle">'+(c/n).toFixed(2)+'</text><text x="'+(i*bw+bw/2)+'" y="'+(H0+13)+'" font-size="9" fill="'+mu+'" text-anchor="middle">'+F(mn+i*w,1)+'</text>'});
      hist+='<line x1="0" y1="'+H0+'" x2="'+W0+'" y2="'+H0+'" stroke="'+tx+'"/></g></svg><div style="font-size:.78rem;color:var(--muted)">Histogram: chiều cao = tần suất tương đối f_rel của từng lớp.</div>';
      var span=(mx-mn)||1,X=function(v){return 20+(v-mn)/span*520},bp='<svg viewBox="0 0 580 90" style="max-width:100%;width:600px"><line x1="'+X(Math.max(mn,lo))+'" y1="40" x2="'+X(q.qL)+'" y2="40" stroke="'+tx+'" stroke-width="2"/><line x1="'+X(q.qU)+'" y1="40" x2="'+X(Math.min(mx,hi))+'" y2="40" stroke="'+tx+'" stroke-width="2"/><rect x="'+X(q.qL)+'" y="22" width="'+Math.max(2,X(q.qU)-X(q.qL))+'" height="36" fill="'+acc+'" opacity=".3" stroke="'+tx+'" stroke-width="2"/><line x1="'+X(q.qM)+'" y1="22" x2="'+X(q.qM)+'" y2="58" stroke="'+css('--accent','#b3122f')+'" stroke-width="3"/>';
      ol.forEach(function(v){bp+='<circle cx="'+X(v)+'" cy="40" r="5" fill="none" stroke="'+css('--bad','#b3122f')+'" stroke-width="2"/>'});
      bp+='<text x="'+X(q.qL)+'" y="78" font-size="11" fill="'+tx+'" text-anchor="middle">qL='+F(q.qL,2)+'</text><text x="'+X(q.qM)+'" y="16" font-size="11" fill="'+css('--accent','#b3122f')+'" text-anchor="middle">qM='+F(q.qM,2)+'</text><text x="'+X(q.qU)+'" y="78" font-size="11" fill="'+tx+'" text-anchor="middle">qU='+F(q.qU,2)+'</text></svg><div style="font-size:.78rem;color:var(--muted)">Boxplot: hộp từ qL đến qU, vạch đỏ là trung vị, vòng tròn đỏ là ngoại lai (tiêu chuẩn 1.5·IQR).</div>';
      var dec=Math.max.apply(null,x.map(function(v){var s=String(v).split('.');return s[1]?s[1].length:0})),sl={};
      sorted.forEach(function(v){var st,lf;if(dec===0){st=Math.floor(Math.abs(v)/10)*(v<0?-1:1);lf=Math.abs(v)%10}else{var t=Math.round(Math.abs(v)*Math.pow(10,dec));st=Math.floor(t/Math.pow(10,dec))*(v<0?-1:1);lf=t%Math.pow(10,dec)}(sl[st]=sl[st]||[]).push(lf)});
      var sk=Object.keys(sl).map(Number).sort(function(a,b){return a-b}),stem='<pre>Stem | Leaf\n'+sk.map(function(k){return String(k).padStart(4,' ')+' | '+sl[k].join(' ')}).join('\n')+'</pre>';
      out.innerHTML='<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px"><div>'+tbl(['Đại lượng','Giá trị'],rows)+'</div><div>'+hist+bp+'<div style="margin-top:6px"><b>Stem-and-leaf</b></div>'+stem+'</div></div>';
    }catch(e){out.innerHTML='<p class="no">'+esc(e.message)+'</p>'}}
  $(root,'#go').onclick=run;$(root,'#pre').onchange=function(){if(this.value){$(root,'#d').value=this.value;run()}};$(root,'#k').onchange=run;run();
};

})();
