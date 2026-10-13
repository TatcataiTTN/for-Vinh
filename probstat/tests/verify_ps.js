// Đối chiếu ps.js với SciPy trên các điểm ngẫu nhiên (cases.json do gen_cases.py tạo)
const PS=require('../_shared/ps.js');const C=require('./cases.json');let bad=0,n=0;
function chk(name,a,b,tol){n++;if(!(Math.abs(a-b)<=tol*Math.max(1,Math.abs(b)))){bad++;if(bad<15)console.log('FAIL',name,a,b)}}
C.norm.forEach(c=>{chk('Phi',PS.normCdf(c[0]),c[1],1e-9);chk('Phi^-1',PS.normInv(c[1]),c[0],1e-7)});
C.t.forEach(c=>{chk('tcdf',PS.tCdf(c[0],c[1]),c[2],1e-8);chk('tcrit',PS.tCrit(c[3],c[1]),c[4],1e-6)});
C.chi2.forEach(c=>{chk('chi2cdf',PS.chi2Cdf(c[0],c[1]),c[2],1e-8);chk('chi2crit',PS.chi2Crit(c[3],c[1]),c[4],1e-6)});
C.binom.forEach(c=>{chk('bpmf',PS.binomPmf(c[0],c[1],c[2]),c[3],1e-9);chk('bcdf',PS.binomCdf(c[0],c[1],c[2]),c[4],1e-9)});
C.pois.forEach(c=>{chk('ppmf',PS.poisPmf(c[0],c[1]),c[2],1e-9);chk('pcdf',PS.poisCdf(c[0],c[1]),c[3],1e-9)});
C.desc.forEach(c=>{const q=PS.quartiles(c.x);chk('mean',PS.mean(c.x),c.mean,1e-12);chk('var',PS.varS(c.x),c.var,1e-12);chk('qL',q.qL,c.qL,1e-12);chk('qU',q.qU,c.qU,1e-12);chk('med',q.qM,c.qM,1e-12)});
console.log(n+' phép so, lỗi: '+bad);process.exit(bad?1:0);
