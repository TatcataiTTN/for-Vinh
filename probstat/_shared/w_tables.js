(function(){'use strict';
var SL=window.SL,PS=SL.PS,frame=SL.frame,$=SL.$,F=SL.F,tbl=SL.tbl,W=window.SIM_W;
/* Bảng tra điện tử: tương đương bảng A7 (Φ), A8 (z), A9 (t) trong đề, thêm χ² */
W.tables=function(root){
  frame(root,'Bảng tra điện tử: Φ(z), U_α, t_α(n), χ²_α(n)',
   '<div class="row"><b>A7 · Φ(z) = P(Z ≤ z):</b> z = <input id="z" type="number" step="any" value="1.5" style="width:90px"> → Φ = <b id="phi"></b></div>'+
   '<div class="row"><b>A8 · giá trị z ứng với xác suất:</b> P(Z ≤ z) = <input id="p" type="number" step="any" value="0.975" style="width:90px"> → z = <b id="zq"></b></div>'+
   '<div class="row"><b>Giá trị tới hạn chuẩn U_α:</b> α = <input id="a1" type="number" step="any" value="0.05" style="width:80px"> → U_α = <b id="ua"></b> &nbsp; (P(Z &gt; U_α) = α; U_{α/2} = <b id="ua2"></b>)</div>'+
   '<div class="row"><b>A9 · Student t_α(n):</b> α = <input id="a2" type="number" step="any" value="0.05" style="width:80px"> bậc tự do n = <input id="n" type="number" value="18" style="width:70px"> → t_α(n) = <b id="ta"></b> &nbsp; (hai phía t_{α/2}(n) = <b id="ta2"></b>)</div>'+
   '<div class="row"><b>χ²_α(n):</b> α = <input id="a3" type="number" step="any" value="0.05" style="width:80px"> n = <input id="k" type="number" value="5" style="width:70px"> → χ²_α(n) = <b id="ca"></b> &nbsp; (χ²_{1−α}(n) = <b id="cb"></b>)</div>'+
   '<p style="font-size:.82rem;color:var(--muted)">Quy ước: giá trị tới hạn t_α(n), χ²_α(n), U_α là điểm có phần đuôi bên phải bằng α. Đề thi Phenikaa ghi U_α với α là phần diện tích bên phải.</p>');
  function run(){
    var z=+$(root,'#z').value,p=+$(root,'#p').value,a1=+$(root,'#a1').value,a2=+$(root,'#a2').value,n=Math.max(1,Math.round(+$(root,'#n').value)),a3=+$(root,'#a3').value,k=Math.max(1,Math.round(+$(root,'#k').value));
    $(root,'#phi').textContent=F(PS.normCdf(z),4);
    $(root,'#zq').textContent=(p>0&&p<1)?F(PS.normInv(p),4):'—';
    $(root,'#ua').textContent=(a1>0&&a1<1)?F(PS.uCrit(a1),4):'—';$(root,'#ua2').textContent=(a1>0&&a1<1)?F(PS.uCrit(a1/2),4):'—';
    $(root,'#ta').textContent=(a2>0&&a2<1)?F(PS.tCrit(a2,n),4):'—';$(root,'#ta2').textContent=(a2>0&&a2<1)?F(PS.tCrit(a2/2,n),4):'—';
    $(root,'#ca').textContent=(a3>0&&a3<1)?F(PS.chi2Crit(a3,k),4):'—';$(root,'#cb').textContent=(a3>0&&a3<1)?F(PS.chi2Crit(1-a3,k),4):'—';
  }
  root.querySelectorAll('input').forEach(function(i){i.oninput=run});run();
};
})();
