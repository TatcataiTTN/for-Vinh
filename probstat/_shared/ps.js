/* Thư viện thống kê thuần JS (không DOM) — chạy trình duyệt và Node; đối chiếu SciPy trong tests/verify_ps.js */
(function(root){
'use strict';
var PS={};
PS.mean=function(x){var s=0;for(var i=0;i<x.length;i++)s+=x[i];return s/x.length};
PS.sorted=function(x){return x.slice().sort(function(a,b){return a-b})};
PS.median=function(x){var s=PS.sorted(x),n=s.length;return n%2?s[(n-1)/2]:(s[n/2-1]+s[n/2])/2};
PS.quartiles=function(x){var s=PS.sorted(x),n=s.length;return {qL:PS.median(s.slice(0,Math.floor(n/2))),qM:PS.median(s),qU:PS.median(s.slice(Math.ceil(n/2)))}};
PS.varS=function(x){var m=PS.mean(x),s=0;x.forEach(function(v){s+=(v-m)*(v-m)});return s/(x.length-1)};
PS.varP=function(x){var m=PS.mean(x),s=0;x.forEach(function(v){s+=(v-m)*(v-m)});return s/x.length};
PS.sdS=function(x){return Math.sqrt(PS.varS(x))};
PS.outliers=function(x){var q=PS.quartiles(x),r=q.qU-q.qL;return PS.sorted(x).filter(function(v){return v<q.qL-1.5*r||v>q.qU+1.5*r})};
/* ---- hàm đặc biệt ---- */
PS.lgamma=function(z){var c=[76.18009172947146,-86.50532032941677,24.01409824083091,-1.231739572450155,0.001208650973866179,-0.000005395239384953];
  var x=z,y=z,t=x+5.5;t-=(x+0.5)*Math.log(t);var s=1.000000000190015;for(var j=0;j<6;j++){y+=1;s+=c[j]/y}return -t+Math.log(2.5066282746310005*s/x)};
PS.erf=function(x){/* Abramowitz-Stegun 7.1.26 quá thô: dùng chuỗi + liên phân số */
  var ax=Math.abs(x),r;
  if(ax<2.5){var t=ax,s=ax,k=0;var term=ax;for(k=1;k<200;k++){term*=-ax*ax/k;var d=term/(2*k+1);s+=d;if(Math.abs(d)<1e-17)break}r=2/Math.sqrt(Math.PI)*s}
  else{/* erfc bằng liên phân số Lentz */var a=ax,f=0;var n=60;f=0;for(var i=n;i>=1;i--)f=i/2/(a+f);var erfc=Math.exp(-a*a)/Math.sqrt(Math.PI)/(a+f);r=1-erfc}
  return x<0?-r:r};
PS.normCdf=function(z){return 0.5*(1+PS.erf(z/Math.SQRT2))};
PS.normPdf=function(z){return Math.exp(-z*z/2)/Math.sqrt(2*Math.PI)};
PS.normInv=function(p){if(p<=0)return -Infinity;if(p>=1)return Infinity;
  var a=[-3.969683028665376e+01,2.209460984245205e+02,-2.759285104469687e+02,1.383577518672690e+02,-3.066479806614716e+01,2.506628277459239e+00],
  b=[-5.447609879822406e+01,1.615858368580409e+02,-1.556989798598866e+02,6.680131188771972e+01,-1.328068155288572e+01],
  c=[-7.784894002430293e-03,-3.223964580411365e-01,-2.400758277161838e+00,-2.549732539343734e+00,4.374664141464968e+00,2.938163982698783e+00],
  d=[7.784695709041462e-03,3.224671290700398e-01,2.445134137142996e+00,3.754408661907416e+00],pl=0.02425,q,r,x;
  if(p<pl){q=Math.sqrt(-2*Math.log(p));x=(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)}
  else if(p<=1-pl){q=p-0.5;r=q*q;x=(((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q/(((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)}
  else{q=Math.sqrt(-2*Math.log(1-p));x=-(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)}
  for(var i=0;i<3;i++){var e=PS.normCdf(x)-p;var u=e*Math.sqrt(2*Math.PI)*Math.exp(x*x/2);x=x-u/(1+x*u/2)}return x};
/* beta không đầy đủ chính quy I_x(a,b) */
PS.betai=function(a,b,x){if(x<=0)return 0;if(x>=1)return 1;
  var bt=Math.exp(PS.lgamma(a+b)-PS.lgamma(a)-PS.lgamma(b)+a*Math.log(x)+b*Math.log(1-x));
  function cf(a,b,x){var qab=a+b,qap=a+1,qam=a-1,c=1,d=1-qab*x/qap;if(Math.abs(d)<1e-300)d=1e-300;d=1/d;var h=d;
    for(var m=1;m<=300;m++){var m2=2*m,aa=m*(b-m)*x/((qam+m2)*(a+m2));d=1+aa*d;if(Math.abs(d)<1e-300)d=1e-300;c=1+aa/c;if(Math.abs(c)<1e-300)c=1e-300;d=1/d;h*=d*c;
      aa=-(a+m)*(qab+m)*x/((a+m2)*(qap+m2));d=1+aa*d;if(Math.abs(d)<1e-300)d=1e-300;c=1+aa/c;if(Math.abs(c)<1e-300)c=1e-300;d=1/d;var del=d*c;h*=del;if(Math.abs(del-1)<3e-16)break}return h}
  return x<(a+1)/(a+b+2)?bt*cf(a,b,x)/a:1-bt*cf(b,a,1-x)/b};
PS.tCdf=function(t,v){var x=v/(v+t*t),p=0.5*PS.betai(v/2,0.5,x);return t>0?1-p:p};
PS.tPdf=function(t,v){return Math.exp(PS.lgamma((v+1)/2)-PS.lgamma(v/2))/Math.sqrt(v*Math.PI)*Math.pow(1+t*t/v,-(v+1)/2)};
function bisect(f,lo,hi,target){for(var i=0;i<200;i++){var mid=(lo+hi)/2;if(f(mid)<target)lo=mid;else hi=mid}return (lo+hi)/2}
PS.tInv=function(p,v){if(p===0.5)return 0;var lo=-1e3,hi=1e3;return bisect(function(x){return PS.tCdf(x,v)},lo,hi,p)};
PS.tCrit=function(alpha,v){return PS.tInv(1-alpha,v)};          /* t_alpha(v): P(T>t)=alpha */
PS.uCrit=function(alpha){return PS.normInv(1-alpha)};            /* U_alpha: P(Z>U)=alpha */
PS.gammaP=function(a,x){if(x<=0)return 0;var gln=PS.lgamma(a);
  if(x<a+1){var ap=a,sum=1/a,del=sum;for(var n=1;n<500;n++){ap++;del*=x/ap;sum+=del;if(Math.abs(del)<Math.abs(sum)*1e-16)break}return sum*Math.exp(-x+a*Math.log(x)-gln)}
  var b=x+1-a,c=1e300,d=1/b,h=d;for(var i=1;i<500;i++){var an=-i*(i-a);b+=2;d=an*d+b;if(Math.abs(d)<1e-300)d=1e-300;c=b+an/c;if(Math.abs(c)<1e-300)c=1e-300;d=1/d;var del2=d*c;h*=del2;if(Math.abs(del2-1)<1e-16)break}
  return 1-Math.exp(-x+a*Math.log(x)-gln)*h};
PS.chi2Cdf=function(x,k){return PS.gammaP(k/2,x/2)};
PS.chi2Pdf=function(x,k){if(x<=0)return 0;return Math.exp((k/2-1)*Math.log(x)-x/2-(k/2)*Math.log(2)-PS.lgamma(k/2))};
PS.chi2Inv=function(p,k){return bisect(function(x){return PS.chi2Cdf(x,k)},0,1e4,p)};
PS.chi2Crit=function(alpha,k){return PS.chi2Inv(1-alpha,k)};   /* chi2_alpha(k): P(X>c)=alpha */
/* rời rạc */
PS.lchoose=function(n,k){return PS.lgamma(n+1)-PS.lgamma(k+1)-PS.lgamma(n-k+1)};
PS.choose=function(n,k){if(k<0||k>n)return 0;var r=1;k=Math.min(k,n-k);for(var i=1;i<=k;i++)r=r*(n-k+i)/i;return Math.round(r)};
PS.binomPmf=function(k,n,p){if(k<0||k>n)return 0;if(p===0)return k===0?1:0;if(p===1)return k===n?1:0;return Math.exp(PS.lchoose(n,k)+k*Math.log(p)+(n-k)*Math.log(1-p))};
PS.binomCdf=function(k,n,p){var s=0;for(var i=0;i<=Math.floor(k);i++)s+=PS.binomPmf(i,n,p);return Math.min(1,s)};
PS.poisPmf=function(k,mu){if(k<0)return 0;return Math.exp(-mu+k*Math.log(mu)-PS.lgamma(k+1))};
PS.poisCdf=function(k,mu){var s=0;for(var i=0;i<=Math.floor(k);i++)s+=PS.poisPmf(i,mu);return Math.min(1,s)};
/* tương quan, hồi quy */
PS.corr=function(x,y){var mx=PS.mean(x),my=PS.mean(y),sxy=0,sxx=0,syy=0;for(var i=0;i<x.length;i++){sxy+=(x[i]-mx)*(y[i]-my);sxx+=(x[i]-mx)*(x[i]-mx);syy+=(y[i]-my)*(y[i]-my)}return sxy/Math.sqrt(sxx*syy)};
PS.linreg=function(x,y){var mx=PS.mean(x),my=PS.mean(y),sxy=0,sxx=0;for(var i=0;i<x.length;i++){sxy+=(x[i]-mx)*(y[i]-my);sxx+=(x[i]-mx)*(x[i]-mx)}var b=sxy/sxx;return {b:b,a:my-b*mx,r:PS.corr(x,y)}};
PS.fmt=function(x,d){if(x===Infinity)return '∞';if(x===-Infinity)return '−∞';var s=(Math.abs(x)<1e-12?0:x).toFixed(d===undefined?4:d);return s.replace('-','−')};
if(typeof module!=='undefined'&&module.exports)module.exports=PS;else root.PS=PS;
})(typeof window!=='undefined'?window:this);
