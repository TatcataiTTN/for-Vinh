const puppeteer=require('puppeteer-core');
(async()=>{const [url,out,w,h,js]=process.argv.slice(2);
 const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new'});
 const p=await b.newPage();await p.setViewport({width:+w||1100,height:+h||900});await p.goto(url,{waitUntil:'networkidle0'});
 if(js)await p.evaluate(js);await new Promise(r=>setTimeout(r,600));await p.screenshot({path:out,fullPage:false});await b.close()})();
