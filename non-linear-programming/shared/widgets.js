/* widgets.js — các công cụ tương tác chạy 100% trình duyệt (không backend).
   Khởi tạo theo thuộc tính data-widget trên phần tử .widget */
(function(){
  'use strict';
  var COL = {ax:'#8892a6', grid:'#e3e8f2', f:'#c0392b', g:'#1d4ed8', ok:'#136f3a', bad:'#a12a2a', feas:'rgba(29,78,216,0.10)', ink:'#1c2330'};

  /* ---------- tiện ích vẽ ---------- */
  function Plot(canvas, xr, yr){
    this.c = canvas; this.ctx = canvas.getContext('2d');
    this.xr = xr; this.yr = yr; this.W = canvas.width; this.H = canvas.height;
  }
  Plot.prototype.sx = function(x){ return (x-this.xr[0])/(this.xr[1]-this.xr[0])*this.W; };
  Plot.prototype.sy = function(y){ return this.H - (y-this.yr[0])/(this.yr[1]-this.yr[0])*this.H; };
  Plot.prototype.wx = function(px){ return this.xr[0] + px/this.W*(this.xr[1]-this.xr[0]); };
  Plot.prototype.wy = function(py){ return this.yr[0] + (this.H-py)/this.H*(this.yr[1]-this.yr[0]); };
  Plot.prototype.clear = function(){ this.ctx.clearRect(0,0,this.W,this.H); this.ctx.fillStyle='#fff'; this.ctx.fillRect(0,0,this.W,this.H); };
  Plot.prototype.axes = function(step){
    var g = this.ctx; g.lineWidth = 1; g.strokeStyle = COL.grid; g.fillStyle = COL.ax; g.font = '11px sans-serif';
    step = step || 1;
    for (var x = Math.ceil(this.xr[0]/step)*step; x <= this.xr[1]+1e-9; x += step){
      g.beginPath(); g.moveTo(this.sx(x),0); g.lineTo(this.sx(x),this.H); g.stroke();
      g.fillText(String(Math.round(x*100)/100), this.sx(x)+2, Math.min(this.H-3, Math.max(11, this.sy(0)+12)));
    }
    for (var y = Math.ceil(this.yr[0]/step)*step; y <= this.yr[1]+1e-9; y += step){
      g.beginPath(); g.moveTo(0,this.sy(y)); g.lineTo(this.W,this.sy(y)); g.stroke();
      if (Math.abs(y)>1e-9) g.fillText(String(Math.round(y*100)/100), Math.min(this.W-24, Math.max(2, this.sx(0)+3)), this.sy(y)-2);
    }
    g.strokeStyle = COL.ax; g.lineWidth = 1.4;
    g.beginPath(); g.moveTo(this.sx(this.xr[0]), this.sy(0)); g.lineTo(this.sx(this.xr[1]), this.sy(0)); g.stroke();
    g.beginPath(); g.moveTo(this.sx(0), this.sy(this.yr[0])); g.lineTo(this.sx(0), this.sy(this.yr[1])); g.stroke();
  };
  Plot.prototype.line = function(x1,y1,x2,y2,color,w,dash){
    var g=this.ctx; g.beginPath(); g.strokeStyle=color; g.lineWidth=w||1.5; g.setLineDash(dash||[]);
    g.moveTo(this.sx(x1),this.sy(y1)); g.lineTo(this.sx(x2),this.sy(y2)); g.stroke(); g.setLineDash([]);
  };
  Plot.prototype.dot = function(x,y,r,color,stroke){
    var g=this.ctx; g.beginPath(); g.fillStyle=color; g.arc(this.sx(x),this.sy(y),r,0,6.2832); g.fill();
    if (stroke){ g.strokeStyle=stroke; g.lineWidth=1.5; g.stroke(); }
  };
  Plot.prototype.arrow = function(x,y,dx,dy,color,w){
    var g=this.ctx, ax=this.sx(x), ay=this.sy(y), bx=this.sx(x+dx), by=this.sy(y+dy);
    var ang=Math.atan2(by-ay,bx-ax), L=9;
    g.strokeStyle=color; g.fillStyle=color; g.lineWidth=w||2;
    g.beginPath(); g.moveTo(ax,ay); g.lineTo(bx,by); g.stroke();
    g.beginPath(); g.moveTo(bx,by); g.lineTo(bx-L*Math.cos(ang-0.4),by-L*Math.sin(ang-0.4));
    g.lineTo(bx-L*Math.cos(ang+0.4),by-L*Math.sin(ang+0.4)); g.closePath(); g.fill();
  };
  Plot.prototype.text = function(s,x,y,color,font){
    var g=this.ctx; g.fillStyle=color||COL.ink; g.font=font||'12px sans-serif'; g.fillText(s,this.sx(x),this.sy(y));
  };
  // đường mức bằng marching squares
  Plot.prototype.contour = function(f, levels, color, n){
    n = n || 90; var g = this.ctx, self = this;
    var xs=[], ys=[], v=[];
    for (var i=0;i<=n;i++){ xs.push(this.xr[0]+(this.xr[1]-this.xr[0])*i/n); }
    for (var j=0;j<=n;j++){ ys.push(this.yr[0]+(this.yr[1]-this.yr[0])*j/n); }
    for (j=0;j<=n;j++){ v.push([]); for (i=0;i<=n;i++){ v[j].push(f(xs[i],ys[j])); } }
    g.strokeStyle=color||'#9aa6c0'; g.lineWidth=1; g.setLineDash([]);
    levels.forEach(function(L){
      g.beginPath();
      for (var j=0;j<n;j++) for (var i=0;i<n;i++){
        var a=v[j][i]-L, b=v[j][i+1]-L, c=v[j+1][i+1]-L, d=v[j+1][i]-L;
        var pts=[];
        function ip(x1,y1,v1,x2,y2,v2){ var t=v1/(v1-v2); return [x1+(x2-x1)*t, y1+(y2-y1)*t]; }
        if ((a>0)!==(b>0)) pts.push(ip(xs[i],ys[j],a,xs[i+1],ys[j],b));
        if ((b>0)!==(c>0)) pts.push(ip(xs[i+1],ys[j],b,xs[i+1],ys[j+1],c));
        if ((c>0)!==(d>0)) pts.push(ip(xs[i+1],ys[j+1],c,xs[i],ys[j+1],d));
        if ((d>0)!==(a>0)) pts.push(ip(xs[i],ys[j+1],d,xs[i],ys[j],a));
        if (pts.length>=2){ g.moveTo(self.sx(pts[0][0]),self.sy(pts[0][1])); g.lineTo(self.sx(pts[1][0]),self.sy(pts[1][1])); }
        if (pts.length===4){ g.moveTo(self.sx(pts[2][0]),self.sy(pts[2][1])); g.lineTo(self.sx(pts[3][0]),self.sy(pts[3][1])); }
      }
      g.stroke();
    });
  };
  // tô miền thoả mãn hàm boolean bằng lưới điểm
  Plot.prototype.shade = function(pred, color, n){
    n = n || 110; var g=this.ctx; g.fillStyle=color;
    var dx=(this.xr[1]-this.xr[0])/n, dy=(this.yr[1]-this.yr[0])/n;
    for (var i=0;i<n;i++) for (var j=0;j<n;j++){
      var x=this.xr[0]+(i+0.5)*dx, y=this.yr[0]+(j+0.5)*dy;
      if (pred(x,y)) g.fillRect(Math.floor(this.sx(x-dx/2)), Math.floor(this.sy(y+dy/2)), Math.ceil(this.W/n)+1, Math.ceil(this.H/n)+1);
    }
  };
  function fmt(x, d){ d = (d===undefined)?4:d; if (Math.abs(x)<1e-12) return '0'; return String(Math.round(x*Math.pow(10,d))/Math.pow(10,d)); }
  function el(html){ var d=document.createElement('div'); d.innerHTML=html; return d.firstElementChild; }
  function ev(node, name, fn){ node.addEventListener(name, fn); }
  function mkcanvas(host, w, h){ var c=document.createElement('canvas'); c.width=w; c.height=h; c.style.width='100%'; c.style.maxWidth=w+'px'; host.appendChild(c); return c; }
  function ptr(canvas, e){
    var r = canvas.getBoundingClientRect(); var t = (e.touches && e.touches[0]) || e;
    return [(t.clientX - r.left) * canvas.width / r.width, (t.clientY - r.top) * canvas.height / r.height];
  }
  function tex(node){ if (window.nlpRenderMath) window.nlpRenderMath(node); }

  /* =========================================================
     1. hessian-lab: nhập ma trận đối xứng 2x2, phân loại dấu
     ========================================================= */
  function hessianLab(host){
    host.innerHTML = '<h3>Phòng thí nghiệm ma trận Hessian 2×2</h3>' +
      '<p>Nhập ma trận đối xứng \\(H=\\begin{pmatrix}a&b\\\\b&c\\end{pmatrix}\\). Hàm \\(f(x)=\\tfrac12x^\\top Hx\\) có Hessian đúng bằng \\(H\\). Hình vẽ tô <span style="color:#1d4ed8"><b>xanh</b></span> nơi \\(f>0\\), <span style="color:#c0392b"><b>đỏ</b></span> nơi \\(f<0\\).</p>' +
      '<div class="wrow"><div class="wcol">' +
      '<label>a <input type="number" id="ha" value="2" step="0.5"></label><label>b <input type="number" id="hb" value="1" step="0.5"></label><label>c <input type="number" id="hc" value="2" step="0.5"></label>' +
      '<p><button data-p="2,1,2">Xác định dương</button> <button data-p="1,1,1">Nửa xác định dương</button> <button data-p="0,1,0">Không xác định</button> <button data-p="-2,0,-1">Xác định âm</button> <button data-p="0,0,-1">Nửa xđ, minor chính = 0</button></p>' +
      '<div class="out" id="hout"></div></div><div class="wcol" id="hcv"></div></div>';
    var cv = mkcanvas(host.querySelector('#hcv'), 420, 420);
    var P = new Plot(cv, [-3,3], [-3,3]);
    function run(){
      var a=parseFloat(host.querySelector('#ha').value)||0, b=parseFloat(host.querySelector('#hb').value)||0, c=parseFloat(host.querySelector('#hc').value)||0;
      var tr=a+c, det=a*c-b*b, disc=Math.sqrt(Math.max(0,((a-c)/2)*((a-c)/2)+b*b));
      var l1=tr/2-disc, l2=tr/2+disc, eps=1e-9, cls;
      if (l1>eps) cls=['xác định dương ⇒ f lồi chặt','ok']; else if (l1>=-eps) cls=['nửa xác định dương ⇒ f lồi (không chặt)','ok'];
      else if (l2<-eps) cls=['xác định âm ⇒ f lõm chặt','no']; else if (l2<=eps) cls=['nửa xác định âm ⇒ f lõm','no']; else cls=['không xác định ⇒ f không lồi cũng không lõm (điểm yên ngựa)','mid'];
      var lead = (a>eps && det>eps) ? 'Sylvester: Δ₁=a>0 và Δ₂=det>0 ⇒ xác định dương.' :
        ((a>=-eps && c>=-eps && det>=-eps) ? 'Mọi minor chính (a, c, det) đều ≥ 0 ⇒ nửa xác định dương (cần xét CẢ a và c, không chỉ a).' : 'Có minor chính âm hoặc Δ₂<0 ⇒ không nửa xác định dương.');
      host.querySelector('#hout').innerHTML =
        '<p>Giá trị riêng: \\(\\lambda_1='+fmt(l1)+'\\), \\(\\lambda_2='+fmt(l2)+'\\)</p>' +
        '<p>Vết \\(a+c='+fmt(tr)+'\\); định thức \\(ac-b^2='+fmt(det)+'\\) (= tích hai giá trị riêng)</p>' +
        '<p>Minor chính: \\(a='+fmt(a)+'\\), \\(c='+fmt(c)+'\\), \\(\\det='+fmt(det)+'\\)</p>' +
        '<p><span class="badge '+cls[1]+'">'+cls[0]+'</span></p><p style="font-size:.88rem">'+lead+'</p>';
      tex(host.querySelector('#hout'));
      P.clear();
      var f=function(x,y){ return 0.5*(a*x*x+2*b*x*y+c*y*y); };
      var n=70, dx=6/n, g=P.ctx;
      for (var i=0;i<n;i++) for (var j=0;j<n;j++){
        var x=-3+(i+.5)*dx, y=-3+(j+.5)*dx, v=f(x,y), s=Math.min(1,Math.abs(v)/6);
        g.fillStyle = v>=0 ? 'rgba(29,78,216,'+(0.08+0.5*s)+')' : 'rgba(192,57,43,'+(0.08+0.5*s)+')';
        g.fillRect(Math.floor(P.sx(x-dx/2)),Math.floor(P.sy(y+dx/2)),Math.ceil(P.W/n)+1,Math.ceil(P.H/n)+1);
      }
      P.axes(1);
      P.contour(f,[-4,-2,-1,-.25,.25,1,2,4],'#556',80);
    }
    host.querySelectorAll('input').forEach(function(i){ ev(i,'input',run); });
    host.querySelectorAll('button[data-p]').forEach(function(b){ ev(b,'click',function(){ var p=b.getAttribute('data-p').split(','); host.querySelector('#ha').value=p[0]; host.querySelector('#hb').value=p[1]; host.querySelector('#hc').value=p[2]; run(); }); });
    run();
  }

  /* =========================================================
     2. jensen-lab: bất đẳng thức Jensen trên đồ thị
     ========================================================= */
  var FUNS = {
    'x²':{f:function(x){return x*x;}, xr:[-2,2], convex:true},
    'eˣ':{f:Math.exp, xr:[-2,2], convex:true},
    '|x|':{f:Math.abs, xr:[-2,2], convex:true},
    'x³':{f:function(x){return x*x*x;}, xr:[-2,2], convex:false},
    'sin x':{f:Math.sin, xr:[-3,3], convex:false},
    '−ln x (x>0)':{f:function(x){return -Math.log(x);}, xr:[0.15,3], convex:true},
    'ln x (x>0)':{f:Math.log, xr:[0.15,3], convex:false}
  };
  function jensenLab(host){
    var opts = Object.keys(FUNS).map(function(k){ return '<option>'+k+'</option>'; }).join('');
    host.innerHTML = '<h3>Kiểm tra bất đẳng thức Jensen</h3><p>Nối hai điểm trên đồ thị bằng một dây cung. Hàm lồi ⇔ đồ thị luôn nằm <b>dưới</b> mọi dây cung: \\(f(\\theta x+(1-\\theta)y)\\le\\theta f(x)+(1-\\theta)f(y)\\).</p>' +
      '<div class="wrow"><div class="wcol"><label>Hàm f: <select id="jf">'+opts+'</select></label>' +
      '<p><label>x <input type="range" id="jx" min="0" max="1" step="0.005" value="0.15"></label><br><label>y <input type="range" id="jy" min="0" max="1" step="0.005" value="0.85"></label><br><label>θ <input type="range" id="jt" min="0" max="1" step="0.01" value="0.4"></label></p>' +
      '<p><button id="jscan">Quét 5000 bộ ba ngẫu nhiên</button></p><div class="out" id="jout"></div></div><div class="wcol" id="jcv"></div></div>';
    var cv = mkcanvas(host.querySelector('#jcv'), 460, 340);
    function run(){
      var name = host.querySelector('#jf').value, F = FUNS[name];
      var u=parseFloat(host.querySelector('#jx').value), v=parseFloat(host.querySelector('#jy').value), th=parseFloat(host.querySelector('#jt').value);
      var x = F.xr[0]+u*(F.xr[1]-F.xr[0]), y = F.xr[0]+v*(F.xr[1]-F.xr[0]);
      var m=-Infinity, M=Infinity, i, X;
      var ys=[]; for (i=0;i<=200;i++){ X=F.xr[0]+(F.xr[1]-F.xr[0])*i/200; ys.push(F.f(X)); }
      var lo=Math.min.apply(null,ys), hi=Math.max.apply(null,ys), pad=(hi-lo)*0.15+0.2;
      var P = new Plot(cv, [F.xr[0]-0.2, F.xr[1]+0.2], [lo-pad, hi+pad]);
      P.clear(); P.axes(1);
      var g=P.ctx; g.beginPath(); g.strokeStyle=COL.g; g.lineWidth=2.5;
      for (i=0;i<=200;i++){ X=F.xr[0]+(F.xr[1]-F.xr[0])*i/200; if(i===0) g.moveTo(P.sx(X),P.sy(F.f(X))); else g.lineTo(P.sx(X),P.sy(F.f(X))); }
      g.stroke();
      P.line(x,F.f(x),y,F.f(y),COL.f,2);
      var z=th*x+(1-th)*y, fz=F.f(z), chord=th*F.f(x)+(1-th)*F.f(y);
      P.dot(x,F.f(x),5,COL.f); P.dot(y,F.f(y),5,COL.f);
      P.dot(z,fz,6,COL.g); P.dot(z,chord,6,COL.f);
      P.line(z,fz,z,chord,'#555',1.5,[4,3]);
      var ok = fz <= chord+1e-12;
      host.querySelector('#jout').innerHTML = '\\(z=\\theta x+(1-\\theta)y='+fmt(z,3)+'\\)<br>\\(f(z)='+fmt(fz,4)+'\\) (điểm xanh, trên đồ thị)<br>\\(\\theta f(x)+(1-\\theta)f(y)='+fmt(chord,4)+'\\) (điểm đỏ, trên dây cung)<br><span class="badge '+(ok?'ok':'no')+'">'+(ok?'Jensen thỏa với bộ ba này':'Jensen VI PHẠM ⇒ f không lồi')+'</span>';
      tex(host.querySelector('#jout'));
    }
    host.querySelectorAll('input,select').forEach(function(i){ ev(i,'input',run); ev(i,'change',run); });
    ev(host.querySelector('#jscan'),'click',function(){
      var F=FUNS[host.querySelector('#jf').value], bad=0, N=5000, ex=null;
      for (var k=0;k<N;k++){
        var a=F.xr[0]+Math.random()*(F.xr[1]-F.xr[0]), b=F.xr[0]+Math.random()*(F.xr[1]-F.xr[0]), t=Math.random();
        if (F.f(t*a+(1-t)*b) > t*F.f(a)+(1-t)*F.f(b)+1e-9){ bad++; if(!ex) ex=[a,b,t]; }
      }
      host.querySelector('#jout').innerHTML += '<hr>Quét '+N+' bộ ba: <b>'+bad+'</b> vi phạm. ' + (bad===0?'<span class="badge ok">Không thấy vi phạm — phù hợp hàm lồi</span>':'<span class="badge no">Có vi phạm — hàm KHÔNG lồi trên đoạn này</span> (ví dụ: x='+fmt(ex[0],2)+', y='+fmt(ex[1],2)+', θ='+fmt(ex[2],2)+')');
    });
    run();
  }

  /* =========================================================
     3. convex-set-lab: dây cung có nằm trong tập không?
     ========================================================= */
  var SETS = {
    'Hình tròn (lồi)': function(x,y){ return x*x+y*y<=1.7*1.7; },
    'Ellipse (lồi)': function(x,y){ return (x/2.2)*(x/2.2)+(y/1.2)*(y/1.2)<=1; },
    'Ngũ giác đều (lồi)': function(x,y){ var ok=true; for (var k=0;k<5;k++){ var a=Math.PI/2+k*2*Math.PI/5+Math.PI/5; if (x*Math.cos(a)+y*Math.sin(a)>1.35*Math.cos(Math.PI/5)) ok=false; } return ok; },
    'Vành khuyên (KHÔNG lồi)': function(x,y){ var r=x*x+y*y; return r<=2.2*2.2 && r>=1*1; },
    'Chữ L (KHÔNG lồi)': function(x,y){ return (x>=-2&&x<=-0.5&&y>=-2&&y<=2) || (x>=-2&&x<=2&&y>=-2&&y<=-0.5); },
    'Hợp hai hình tròn rời (KHÔNG lồi)': function(x,y){ return (x+1.6)*(x+1.6)+y*y<=1 || (x-1.6)*(x-1.6)+y*y<=1; },
    'Giao: nửa mặt phẳng ∩ hình tròn (lồi)': function(x,y){ return x+y<=1 && x*x+y*y<=2.3*2.3; }
  };
  function convexSetLab(host){
    var opts = Object.keys(SETS).map(function(k){ return '<option>'+k+'</option>'; }).join('');
    host.innerHTML = '<h3>Tập nào lồi? Thử nối hai điểm</h3><p>Chọn một tập, <b>bấm hoặc kéo</b> trên hình để đặt hai điểm A, B trong tập. Nếu có một điểm nào của đoạn AB rơi ra ngoài thì tập không lồi.</p>' +
      '<div class="wrow"><div class="wcol"><label>Tập: <select id="sset">'+opts+'</select></label><p><button id="srand">Tìm cặp vi phạm (5000 lần thử)</button></p><div class="out" id="sout">Bấm vào hình để đặt A rồi B.</div></div><div class="wcol" id="scv"></div></div>';
    var cv = mkcanvas(host.querySelector('#scv'), 440, 440);
    var P = new Plot(cv, [-3,3], [-3,3]);
    var A=null, B=null, next='A';
    function inside(x,y){ return SETS[host.querySelector('#sset').value](x,y); }
    function draw(){
      P.clear(); P.shade(inside,'rgba(29,78,216,0.22)',130); P.axes(1);
      if (A) P.dot(A[0],A[1],6,COL.g);
      if (B) P.dot(B[0],B[1],6,COL.g);
      if (A){ P.text('A',A[0]+.08,A[1]+.12); }
      if (B){ P.text('B',B[0]+.08,B[1]+.12); }
      if (A && B){
        var bad=null, N=300;
        for (var i=0;i<=N;i++){ var t=i/N, x=A[0]*(1-t)+B[0]*t, y=A[1]*(1-t)+B[1]*t; if(!inside(x,y)){ bad=[x,y]; break; } }
        var okAB = inside(A[0],A[1]) && inside(B[0],B[1]);
        P.line(A[0],A[1],B[0],B[1], bad?COL.bad:COL.ok, 3);
        if (bad) P.dot(bad[0],bad[1],6,COL.bad,'#fff');
        host.querySelector('#sout').innerHTML = !okAB ? '<span class="badge mid">Hãy đặt A và B bên TRONG tập (vùng xanh)</span>' :
          (bad ? '<span class="badge no">Có điểm của đoạn AB nằm ngoài tập ⇒ tập KHÔNG lồi</span>' : '<span class="badge ok">Đoạn AB nằm trọn trong tập (với cặp này)</span><br>Một cặp thỏa chưa chứng minh được tính lồi — phải đúng với MỌI cặp.');
      }
    }
    function place(e){
      var p = ptr(cv,e), x=P.wx(p[0]), y=P.wy(p[1]);
      if (next==='A'){ A=[x,y]; B=null; next='B'; } else { B=[x,y]; next='A'; }
      draw(); e.preventDefault();
    }
    ev(cv,'mousedown',place); ev(cv,'touchstart',place);
    ev(host.querySelector('#sset'),'change',function(){ A=B=null; next='A'; host.querySelector('#sout').textContent='Bấm vào hình để đặt A rồi B.'; draw(); });
    ev(host.querySelector('#srand'),'click',function(){
      var found=null, tries=0;
      while (tries++<5000 && !found){
        var a=[Math.random()*6-3,Math.random()*6-3], b=[Math.random()*6-3,Math.random()*6-3];
        if (!inside(a[0],a[1])||!inside(b[0],b[1])) continue;
        for (var i=1;i<100;i++){ var t=i/100; if(!inside(a[0]*(1-t)+b[0]*t,a[1]*(1-t)+b[1]*t)){ found=[a,b]; break; } }
      }
      if (found){ A=found[0]; B=found[1]; next='A'; draw(); }
      else { host.querySelector('#sout').innerHTML='<span class="badge ok">Không tìm thấy cặp vi phạm sau 5000 lần thử — phù hợp tập lồi</span>'; }
    });
    draw();
  }

  /* =========================================================
     4. kkt-lab: thử điểm có phải điểm KKT không
     ========================================================= */
  var KKT = {
    'Ví dụ 1 (slide tr.55): min (x−1)²+y−2; x+y−2≤0; x−y+1=0': {
      xr:[-2,3.2], yr:[-1,4.2],
      f:function(x,y){return (x-1)*(x-1)+y-2;}, gf:function(x,y){return [2*(x-1),1];},
      cons:[{k:'ineq',lab:'g₁ = x+y−2 ≤ 0',g:function(x,y){return x+y-2;},gg:function(){return [1,1];}},
            {k:'eq',lab:'h₁ = x−y+1 = 0',g:function(x,y){return x-y+1;},gg:function(){return [1,-1];}}],
      cand:[[0.5,1.5]], levels:[-1.5,-1,-0.5,-0.25,0,1,2,4]},
    'Ví dụ 3 (slide tr.60): min xy; x²+y²≤2': {
      xr:[-2.2,2.2], yr:[-2.2,2.2],
      f:function(x,y){return x*y;}, gf:function(x,y){return [y,x];},
      cons:[{k:'ineq',lab:'g₁ = x²+y²−2 ≤ 0',g:function(x,y){return x*x+y*y-2;},gg:function(x,y){return [2*x,2*y];}}],
      cand:[[0,0],[1,-1],[-1,1],[1,1],[-1,-1]], levels:[-1.5,-1,-0.5,0,0.5,1,1.5]},
    'Ví dụ 4 (slide tr.61): min 2x+y; 3x+y≤6; x+y≤4; x,y≥0': {
      xr:[-1,4.2], yr:[-1,6],
      f:function(x,y){return 2*x+y;}, gf:function(){return [2,1];},
      cons:[{k:'ineq',lab:'g₁ = 3x+y−6 ≤ 0',g:function(x,y){return 3*x+y-6;},gg:function(){return [3,1];}},
            {k:'ineq',lab:'g₂ = x+y−4 ≤ 0',g:function(x,y){return x+y-4;},gg:function(){return [1,1];}},
            {k:'ineq',lab:'g₃ = −x ≤ 0',g:function(x,y){return -x;},gg:function(){return [-1,0];}},
            {k:'ineq',lab:'g₄ = −y ≤ 0',g:function(x,y){return -y;},gg:function(){return [0,-1];}}],
      cand:[[0,0],[2,0],[1,3],[0,4]], levels:[1,2,3,4,5,6,7,8]},
    'Ví dụ 2 dạng cực tiểu −f (slide tr.57): min −(x²+y²+4x−6y); x+y≤3; −2x+y≤2': {
      xr:[-4,4], yr:[-2,6],
      f:function(x,y){return -(x*x+y*y+4*x-6*y);}, gf:function(x,y){return [-2*x-4,-2*y+6];},
      cons:[{k:'ineq',lab:'g₁ = x+y−3 ≤ 0',g:function(x,y){return x+y-3;},gg:function(){return [1,1];}},
            {k:'ineq',lab:'g₂ = −2x+y−2 ≤ 0',g:function(x,y){return -2*x+y-2;},gg:function(){return [-2,1];}}],
      cand:[[1/3,8/3],[0,2],[-2,3]], levels:[-30,-20,-13,-8,-4,0,4,8]},
    'Bài luyện C9 (tham khảo): min 3x²+3y²−4xy; −x−y+2≤0; x²+y²−4≤0': {
      xr:[-3,3], yr:[-3,3],
      f:function(x,y){return 3*x*x+3*y*y-4*x*y;}, gf:function(x,y){return [6*x-4*y,6*y-4*x];},
      cons:[{k:'ineq',lab:'g₁ = −x−y+2 ≤ 0',g:function(x,y){return -x-y+2;},gg:function(){return [-1,-1];}},
            {k:'ineq',lab:'g₂ = x²+y²−4 ≤ 0',g:function(x,y){return x*x+y*y-4;},gg:function(x,y){return [2*x,2*y];}}],
      cand:[[1,1],[1.2,1.2]], levels:[1,2,4,8,12,16,24]},
    'Bài luyện C10 (tham khảo): min 4x²+y²−x−2y; 2x+y≤1; x²−1≤0': {
      xr:[-2,2], yr:[-1.5,3],
      f:function(x,y){return 4*x*x+y*y-x-2*y;}, gf:function(x,y){return [8*x-1,2*y-2];},
      cons:[{k:'ineq',lab:'g₁ = 2x+y−1 ≤ 0',g:function(x,y){return 2*x+y-1;},gg:function(){return [2,1];}},
            {k:'ineq',lab:'g₂ = x²−1 ≤ 0',g:function(x,y){return x*x-1;},gg:function(x){return [2*x,0];}}],
      cand:[[1/16,7/8],[0.125,1]], levels:[-1,-0.5,0,1,2,4,8]}
  };
  function solveLS(vs, rhs){ // min ||sum lam_i v_i - rhs|| với vs: mảng vector 2D
    var k = vs.length; if (k===0) return {lam:[], res:Math.hypot(rhs[0],rhs[1])};
    var M=[], b=[], i, j;
    for (i=0;i<k;i++){ M.push([]); for (j=0;j<k;j++) M[i].push(vs[i][0]*vs[j][0]+vs[i][1]*vs[j][1]); b.push(vs[i][0]*rhs[0]+vs[i][1]*rhs[1]); }
    for (i=0;i<k;i++) M[i][i]+=1e-12;
    // Gauss
    for (i=0;i<k;i++){
      var p=i; for (j=i+1;j<k;j++) if (Math.abs(M[j][i])>Math.abs(M[p][i])) p=j;
      var tmp=M[i]; M[i]=M[p]; M[p]=tmp; var tb=b[i]; b[i]=b[p]; b[p]=tb;
      for (j=i+1;j<k;j++){ var f=M[j][i]/M[i][i]; for (var c=i;c<k;c++) M[j][c]-=f*M[i][c]; b[j]-=f*b[i]; }
    }
    var lam=new Array(k);
    for (i=k-1;i>=0;i--){ var s=b[i]; for (j=i+1;j<k;j++) s-=M[i][j]*lam[j]; lam[i]=s/M[i][i]; }
    var r=[-rhs[0],-rhs[1]]; for (i=0;i<k;i++){ r[0]+=lam[i]*vs[i][0]; r[1]+=lam[i]*vs[i][1]; }
    return {lam:lam, res:Math.hypot(r[0],r[1])};
  }
  function kktLab(host){
    var names = Object.keys(KKT);
    host.innerHTML = '<h3>Phòng thí nghiệm KKT (2 biến)</h3><p>Chọn bài toán, nhập điểm \\((x,y)\\) hoặc bấm lên hình. Công cụ tìm các ràng buộc <b>chặt</b>, giải \\(\\nabla f+\\sum\\lambda_i\\nabla g_i+\\sum\\mu_j\\nabla h_j=0\\) bằng bình phương tối thiểu và kiểm tra dấu \\(\\lambda\\ge0\\).</p>' +
      '<div class="wrow"><div class="wcol"><label>Bài: <select id="kp" style="max-width:100%">'+names.map(function(n){return '<option>'+n+'</option>';}).join('')+'</select></label>' +
      '<p><label>x <input type="number" id="kx" step="0.05" value="0.5"></label> <label>y <input type="number" id="ky" step="0.05" value="1.5"></label></p>' +
      '<p id="kcand"></p><div class="out" id="kout"></div></div><div class="wcol" id="kcv"></div></div>' +
      '<p style="font-size:.85rem;color:var(--muted)">Mũi tên đỏ: ∇f; mũi tên xanh: ∇g<sub>i</sub> của các ràng buộc chặt. Tại điểm KKT của bài min, ∇f nằm trong nón sinh bởi −∇g<sub>i</sub> (ngược hướng các gradient ràng buộc chặt).</p>';
    var cv = mkcanvas(host.querySelector('#kcv'), 460, 460), P;
    function cur(){ return KKT[host.querySelector('#kp').value]; }
    function setup(){
      var pr=cur(); P = new Plot(cv, pr.xr, pr.yr);
      var cs=host.querySelector('#kcand'); cs.innerHTML='Điểm gợi ý: ';
      pr.cand.forEach(function(c){ var b=document.createElement('button'); b.type='button'; b.textContent='('+fmt(c[0],3)+', '+fmt(c[1],3)+')';
        ev(b,'click',function(){ host.querySelector('#kx').value=c[0]; host.querySelector('#ky').value=c[1]; run(); }); cs.appendChild(b); cs.appendChild(document.createTextNode(' ')); });
      var d=pr.cand[0]; host.querySelector('#kx').value=d[0]; host.querySelector('#ky').value=d[1];
    }
    function feas(pr,x,y,tol){ return pr.cons.every(function(c){ var v=c.g(x,y); return c.k==='eq' ? Math.abs(v)<=tol : v<=tol; }); }
    function run(){
      var pr=cur(), x=parseFloat(host.querySelector('#kx').value), y=parseFloat(host.querySelector('#ky').value);
      if (isNaN(x)||isNaN(y)) return;
      P.clear();
      P.shade(function(a,b){ return feas(pr,a,b,0); }, COL.feas, 120);
      P.axes(1);
      P.contour(pr.f, pr.levels, '#aab', 90);
      pr.cons.forEach(function(c){ // vẽ biên ràng buộc
        P.contour(c.g,[0], c.k==='eq'?'#7a3ed0':'#1d4ed8', 120); P.ctx.lineWidth=1;
      });
      var tol=1e-6, act=[], vs=[], k;
      pr.cons.forEach(function(c,i){ var v=c.g(x,y); if (c.k==='eq' || Math.abs(v)<=tol) act.push(i); });
      var okF = feas(pr,x,y,tol);
      var gf=pr.gf(x,y), rhs=[-gf[0],-gf[1]];
      act.forEach(function(i){ vs.push(pr.cons[i].gg(x,y)); });
      var ls=solveLS(vs,rhs);
      var sc = 0.9/Math.max(1,Math.hypot(gf[0],gf[1]));
      P.arrow(x,y,gf[0]*sc,gf[1]*sc,COL.f,2.5);
      act.forEach(function(i){ var g=pr.cons[i].gg(x,y); var s=0.9/Math.max(1,Math.hypot(g[0],g[1])); P.arrow(x,y,g[0]*s,g[1]*s,COL.g,2); });
      P.dot(x,y,6, okF?COL.ok:COL.bad,'#fff');
      var html = '<p>Khả thi: <span class="badge '+(okF?'ok':'no')+'">'+(okF?'có':'không')+'</span></p>';
      html += '<p>Ràng buộc chặt: '+(act.length?act.map(function(i){return pr.cons[i].lab;}).join('; '):'<i>không có</i>')+'</p>';
      html += '<p>\\(\\nabla f='+'('+fmt(gf[0])+',\\ '+fmt(gf[1])+')\\)</p>';
      var ok=false;
      if (okF){
        var ineqOK=true, txt=[];
        act.forEach(function(i,ix){ var lam=ls.lam[ix]; txt.push('\\(\\'+(pr.cons[i].k==='eq'?'mu':'lambda')+'_{'+(i+1)+'}='+fmt(lam,4)+'\\)'); if (pr.cons[i].k==='ineq' && lam < -1e-6) ineqOK=false; });
        var stat = ls.res < 1e-5;
        html += '<p>Nhân tử (bình phương tối thiểu): '+(txt.length?txt.join(', '):'—')+'; dư \\(\\|\\nabla f+\\sum\\lambda\\nabla g\\|='+fmt(ls.res,6)+'\\)</p>';
        ok = stat && ineqOK;
        html += '<p><span class="badge '+(ok?'ok':(stat?'mid':'no'))+'">'+(ok?'ĐÂY LÀ ĐIỂM KKT (dừng, λ ≥ 0)':(stat?'Dừng nhưng có λ<0 ⇒ không phải KKT':'∇f không nằm trong nón ràng buộc ⇒ không KKT'))+'</span></p>';
      } else html += '<p><span class="badge no">Không khả thi ⇒ không thể là KKT</span></p>';
      host.querySelector('#kout').innerHTML = html; tex(host.querySelector('#kout'));
    }
    ev(host.querySelector('#kp'),'change',function(){ setup(); run(); });
    host.querySelectorAll('#kx,#ky').forEach(function(i){ ev(i,'input',run); });
    function pick(e){ var p=ptr(cv,e), x=Math.round(P.wx(p[0])*20)/20, y=Math.round(P.wy(p[1])*20)/20; host.querySelector('#kx').value=x; host.querySelector('#ky').value=y; run(); e.preventDefault(); }
    ev(cv,'mousedown',pick); ev(cv,'touchstart',pick);
    setup(); run();
  }

  /* =========================================================
     5. active-set-stepper: lần theo vết thuật toán tập hoạt động
     ========================================================= */
  function activeSetStepper(host){
    var data = JSON.parse(host.querySelector('script[type="application/json"]').textContent);
    var names = Object.keys(data);
    host.querySelector('script').remove();
    host.insertAdjacentHTML('afterbegin','<h3>Duyệt từng bước thuật toán tập hoạt động</h3>');
    host.insertAdjacentHTML('beforeend','<div class="wrow"><div class="wcol"><label>Bài: <select id="as-p">'+names.map(function(n){return '<option>'+n+'</option>';}).join('')+'</select></label> ' +
      '<button id="as-prev">◀ Bước trước</button> <button id="as-next">Bước sau ▶</button> <span id="as-k"></span><div class="out" id="as-out"></div></div><div class="wcol" id="as-cv"></div></div>');
    var cv = mkcanvas(host.querySelector('#as-cv'), 460, 400), P, D, k=0;
    function clip(poly, a, b){ // giữ nửa mặt phẳng a·x <= b
      var out=[]; for (var i=0;i<poly.length;i++){ var p=poly[i], q=poly[(i+1)%poly.length]; var fp=a[0]*p[0]+a[1]*p[1]-b, fq=a[0]*q[0]+a[1]*q[1]-b;
        if (fp<=0) out.push(p); if ((fp<0&&fq>0)||(fp>0&&fq<0)){ var t=fp/(fp-fq); out.push([p[0]+t*(q[0]-p[0]), p[1]+t*(q[1]-p[1])]); } } return out; }
    function load(){
      D = data[host.querySelector('#as-p').value]; k=0; P = new Plot(cv, D.xr, D.yr); draw();
    }
    function feasible(x,y){ return D.A.every(function(a,i){ return a[0]*x+a[1]*y<=D.b[i]+1e-9; }); }
    function draw(){
      var L=D.log, s=L[k], g=P.ctx; P.clear(); P.shade(feasible,'rgba(29,78,216,0.12)',110); P.axes(1);
      P.contour(function(x,y){ return 0.5*(D.Q[0][0]*x*x+2*D.Q[0][1]*x*y+D.Q[1][1]*y*y)+D.c[0]*x+D.c[1]*y; }, D.levels, '#b7bfd4', 90);
      D.A.forEach(function(a,i){
        var inW = s.W.indexOf(i+1)>=0;
        // vẽ đường a·x=b trong khung
        var pts=[]; [[D.xr[0],null],[D.xr[1],null]].forEach(function(){});
        var seg=[]; var xr=D.xr, yr=D.yr;
        if (Math.abs(a[1])>1e-12){ seg.push([xr[0],(D.b[i]-a[0]*xr[0])/a[1]]); seg.push([xr[1],(D.b[i]-a[0]*xr[1])/a[1]]); }
        else { seg.push([D.b[i]/a[0],yr[0]]); seg.push([D.b[i]/a[0],yr[1]]); }
        P.line(seg[0][0],seg[0][1],seg[1][0],seg[1][1], inW?'#c0392b':'#7a86a3', inW?3.2:1.3, inW?[]:[5,4]);
      });
      // đường đi
      for (var j=0;j<=k;j++){ var t=L[j]; if (t.x_next && j<k){ P.line(t.x[0],t.x[1],t.x_next[0],t.x_next[1],'#136f3a',2.6); } }
      for (j=0;j<=k;j++){ P.dot(L[j].x[0],L[j].x[1], j===k?7:4, j===k?'#c0392b':'#136f3a', '#fff'); }
      if (s.x_next){ P.dot(s.x_next[0],s.x_next[1],5,'rgba(19,111,58,.45)'); P.arrow(s.x[0],s.x[1],s.d[0]*(s.alpha||1),s.d[1]*(s.alpha||1),'#136f3a',2); }
      if (D.opt) { P.dot(D.opt[0],D.opt[1],5,'#7a3ed0'); }
      host.querySelector('#as-k').textContent = ' Vòng k = '+s.k+' ('+(k+1)+'/'+L.length+')';
      var h = '<p>\\(x^{k}=('+s.x.map(function(v){return fmt(v,4);}).join(',\\ ')+')\\), tập làm việc \\(W_k=\\{'+s.W.join(',')+'\\}\\)</p>' +
        '<p>\\(g^k=Qx^k+c=('+s.g.map(function(v){return fmt(v,4);}).join(',\\ ')+')\\)</p>' +
        '<p>Bài toán con (ràng buộc \\(a_i^\\top d=0,\\ i\\in W_k\\)) cho \\(d^k=('+s.d.map(function(v){return fmt(v,4);}).join(',\\ ')+')\\)</p>';
      if (s.mu){ h += '<p>\\(d^k=0\\) ⇒ tính nhân tử: '+Object.keys(s.mu).map(function(i){ return '\\(\\hat\\mu_'+i+'='+fmt(s.mu[i],4)+'\\)'; }).join(', ')+'</p>'; }
      if (s.alpha!==undefined){ h += '<p>Bước \\(\\alpha_k='+fmt(s.alpha,4)+'\\)</p>'; }
      h += '<p><b>'+s.action+'</b></p>';
      if (s.f!==undefined) h += '<p style="font-size:.85rem">\\(\\tfrac12x^\\top Qx+c^\\top x='+fmt(s.f,4)+'\\)</p>';
      host.querySelector('#as-out').innerHTML = h; tex(host.querySelector('#as-out'));
      host.querySelector('#as-prev').disabled = (k===0); host.querySelector('#as-next').disabled = (k===L.length-1);
    }
    ev(host.querySelector('#as-p'),'change',load);
    ev(host.querySelector('#as-prev'),'click',function(){ if(k>0){k--;draw();} });
    ev(host.querySelector('#as-next'),'click',function(){ if(k<D.log.length-1){k++;draw();} });
    load();
  }

  /* =========================================================
     6. qp-eq-solver: giải QP ràng buộc đẳng thức qua hệ KKT
     ========================================================= */
  function parseMat(t){ return t.trim().split(/\n+/).map(function(r){ return r.trim().split(/[\s,;]+/).map(Number); }); }
  function gauss(M, b){
    var n=M.length, A=M.map(function(r,i){ return r.concat([b[i]]); }), i,j,k;
    for (i=0;i<n;i++){
      var p=i; for (j=i+1;j<n;j++) if (Math.abs(A[j][i])>Math.abs(A[p][i])) p=j;
      if (Math.abs(A[p][i])<1e-12) return null;
      var t=A[i]; A[i]=A[p]; A[p]=t;
      for (j=i+1;j<n;j++){ var f=A[j][i]/A[i][i]; for (k=i;k<=n;k++) A[j][k]-=f*A[i][k]; }
    }
    var x=new Array(n);
    for (i=n-1;i>=0;i--){ var s=A[i][n]; for (j=i+1;j<n;j++) s-=A[i][j]*x[j]; x[i]=s/A[i][i]; }
    return x;
  }
  function qpEqSolver(host){
    host.innerHTML = '<h3>Giải QP ràng buộc đẳng thức: \\(\\min\\ \\tfrac12x^\\top Qx+c^\\top x\\ \\text{s.t.}\\ Ax=b\\)</h3>' +
      '<p>Công cụ giải hệ KKT \\(\\begin{pmatrix}Q&A^\\top\\\\A&0\\end{pmatrix}\\begin{pmatrix}x\\\\\\mu\\end{pmatrix}=\\begin{pmatrix}-c\\\\b\\end{pmatrix}\\) (bằng Gauss, tương đương phương pháp không gian hạt nhân khi nghiệm duy nhất).</p>' +
      '<div class="wrow"><div class="wcol"><label>Q (mỗi dòng một hàng)</label><br><textarea id="qq" rows="4" cols="22">2 -2 -1\n-2 2 1\n-1 1 5</textarea><br>' +
      '<label>c</label> <input type="text" id="qc" value="10 -26 -2" size="18"><br><label>A</label><br><textarea id="qa" rows="3" cols="22">1 1 0\n1 0 1</textarea><br><label>b</label> <input type="text" id="qb" value="4 10" size="18">' +
      '<p><button id="qrun">Giải</button> <button id="qbt">Bài tập (b=(3,0))</button></p></div><div class="wcol"><div class="out" id="qout">Bấm “Giải”.</div></div></div>';
    function run(){
      try{
        var Q=parseMat(host.querySelector('#qq').value), c=host.querySelector('#qc').value.trim().split(/[\s,;]+/).map(Number),
            A=parseMat(host.querySelector('#qa').value), b=host.querySelector('#qb').value.trim().split(/[\s,;]+/).map(Number);
        var n=Q.length, m=A.length, i,j;
        for (i=0;i<n;i++) for (j=0;j<i;j++) if (Math.abs(Q[i][j]-Q[j][i])>1e-9) throw new Error('Q không đối xứng ở ('+(i+1)+','+(j+1)+')');
        var K=[], rhs=[];
        for (i=0;i<n;i++){ K.push(Q[i].concat(A.map(function(r){return r[i];}))); rhs.push(-c[i]); }
        for (i=0;i<m;i++){ K.push(A[i].concat(new Array(m).fill(0))); rhs.push(b[i]); }
        var sol=gauss(K,rhs);
        if (!sol){ host.querySelector('#qout').innerHTML='<span class="badge no">Hệ KKT suy biến</span> (ZᵀQZ không xác định dương, hoặc A không đủ hạng hàng).'; return; }
        var x=sol.slice(0,n), mu=sol.slice(n);
        var f=0; for (i=0;i<n;i++){ for (j=0;j<n;j++) f+=0.5*x[i]*Q[i][j]*x[j]; f+=c[i]*x[i]; }
        host.querySelector('#qout').innerHTML='<p>\\(x^*=('+x.map(function(v){return fmt(v,4);}).join(',\\ ')+')\\)</p><p>\\(\\mu^*=('+mu.map(function(v){return fmt(v,4);}).join(',\\ ')+')\\)</p><p>\\(f(x^*)=\\tfrac12x^{*\\top}Qx^*+c^\\top x^*='+fmt(f,4)+'\\)</p>'+
          '<p style="font-size:.85rem">Kiểm tra: \\(Ax^*=('+A.map(function(r){ return fmt(r.reduce(function(s,v,k){return s+v*x[k];},0),4); }).join(',\\ ')+')\\) so với \\(b\\).</p>';
        tex(host.querySelector('#qout'));
      }catch(e){ host.querySelector('#qout').innerHTML='<span class="badge no">Lỗi nhập liệu</span> '+e.message; }
    }
    ev(host.querySelector('#qrun'),'click',run);
    ev(host.querySelector('#qbt'),'click',function(){
      host.querySelector('#qq').value='6 2 1\n2 5 2\n1 2 4'; host.querySelector('#qc').value='-8 -3 -3';
      host.querySelector('#qa').value='1 0 1\n0 1 1'; host.querySelector('#qb').value='3 0'; run();
    });
    run();
  }

  /* =========================================================
     7. grad-lab: gradient, hướng giảm nhanh nhất, gradient descent
     ========================================================= */
  var GF = {
    'x² + 3y²': {f:function(x,y){return x*x+3*y*y;}, g:function(x,y){return [2*x,6*y];}, L:6, lv:[0.5,1,2,4,8,14]},
    'x² + y² (đường mức tròn)': {f:function(x,y){return x*x+y*y;}, g:function(x,y){return [2*x,2*y];}, L:2, lv:[0.5,1,2,4,8,14]},
    'Hàm Rosenbrock rút gọn (x−1)²+5(y−x²)²': {f:function(x,y){return (x-1)*(x-1)+5*(y-x*x)*(y-x*x);}, g:function(x,y){return [2*(x-1)-20*x*(y-x*x),10*(y-x*x)];}, L:40, lv:[0.2,0.6,1.5,3,6,12,20]}
  };
  function gradLab(host){
    host.innerHTML='<h3>Gradient, đường mức và hướng giảm</h3><p>Bấm lên hình để chọn điểm \\(p\\). Mũi tên đỏ là \\(\\nabla f(p)\\) (vuông góc đường mức, hướng tăng nhanh nhất), mũi tên xanh là \\(-\\nabla f(p)\\). Nút “Chạy gradient descent” đi \\(x\\leftarrow x-t\\nabla f(x)\\).</p>' +
      '<div class="wrow"><div class="wcol"><label>Hàm: <select id="gf">'+Object.keys(GF).map(function(k){return '<option>'+k+'</option>';}).join('')+'</select></label><p><label>Bước t <input type="range" id="gt" min="0.01" max="0.6" step="0.01" value="0.1"> <span id="gtv">0.10</span></label></p><p><button id="grun">Chạy gradient descent (30 bước)</button></p><div class="out" id="gout"></div></div><div class="wcol" id="gcv"></div></div>';
    var cv=mkcanvas(host.querySelector('#gcv'),440,440), P=new Plot(cv,[-2.5,2.5],[-2.5,2.5]), pt=[-1.8,1.4], path=[];
    function cur(){ return GF[host.querySelector('#gf').value]; }
    function draw(){
      var F=cur(); P.clear(); P.axes(1); P.contour(F.f,F.lv,'#8d99b8',100);
      if (path.length){ for (var i=1;i<path.length;i++) P.line(path[i-1][0],path[i-1][1],path[i][0],path[i][1],'#136f3a',2); path.forEach(function(p){P.dot(p[0],p[1],3,'#136f3a');}); }
      var g=F.g(pt[0],pt[1]), n=Math.hypot(g[0],g[1]), s=n>0?0.9/n:0;
      P.arrow(pt[0],pt[1],g[0]*s,g[1]*s,COL.f,2.5); P.arrow(pt[0],pt[1],-g[0]*s,-g[1]*s,COL.g,2.5); P.dot(pt[0],pt[1],6,'#222','#fff');
      host.querySelector('#gout').innerHTML='\\(p=('+fmt(pt[0],3)+',\\ '+fmt(pt[1],3)+')\\), \\(f(p)='+fmt(F.f(pt[0],pt[1]),4)+'\\)<br>\\(\\nabla f(p)=('+fmt(g[0],3)+',\\ '+fmt(g[1],3)+')\\), \\(\\|\\nabla f(p)\\|='+fmt(n,3)+'\\)' + (path.length?('<br>Sau '+(path.length-1)+' bước: \\(f='+fmt(F.f(path[path.length-1][0],path[path.length-1][1]),6)+'\\)'):'') + '<br><span style="font-size:.85rem">Bước quá lớn (t > 2/L, L=hằng số Lipschitz của ∇f) làm dãy dao động/phân kỳ.</span>';
      tex(host.querySelector('#gout'));
    }
    function pick(e){ var p=ptr(cv,e); pt=[P.wx(p[0]),P.wy(p[1])]; path=[]; draw(); e.preventDefault(); }
    ev(cv,'mousedown',pick); ev(cv,'touchstart',pick);
    ev(host.querySelector('#gf'),'change',function(){ path=[]; draw(); });
    ev(host.querySelector('#gt'),'input',function(){ host.querySelector('#gtv').textContent=parseFloat(this.value).toFixed(2); });
    ev(host.querySelector('#grun'),'click',function(){
      var F=cur(), t=parseFloat(host.querySelector('#gt').value), x=pt.slice(); path=[x.slice()];
      for (var i=0;i<30;i++){ var g=F.g(x[0],x[1]); x=[x[0]-t*g[0], x[1]-t*g[1]]; if (!isFinite(x[0])||Math.abs(x[0])>50||Math.abs(x[1])>50) break; path.push(x.slice()); }
      draw();
    });
    draw();
  }

  var REG = {'hessian-lab':hessianLab,'jensen-lab':jensenLab,'convex-set-lab':convexSetLab,'kkt-lab':kktLab,
             'active-set-stepper':activeSetStepper,'qp-eq-solver':qpEqSolver,'grad-lab':gradLab};
  function boot(){
    document.querySelectorAll('.widget[data-widget]').forEach(function(h){
      var fn = REG[h.getAttribute('data-widget')];
      if (fn){ try{ fn(h); tex(h); }catch(e){ console.error('widget error', h.getAttribute('data-widget'), e); h.insertAdjacentHTML('beforeend','<p class="badge no">Lỗi widget: '+e.message+'</p>'); } }
    });
  }
  if (document.readyState==='loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
