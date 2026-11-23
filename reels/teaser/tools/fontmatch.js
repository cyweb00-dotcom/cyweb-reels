const {chromium}=require('playwright');const fs=require('fs');
const fams=[['Barlow Condensed',600,'barlow-condensed'],['Barlow Condensed',700,'barlow-condensed'],['Barlow Condensed',800,'barlow-condensed'],['Oswald',500,'oswald'],['Oswald',600,'oswald'],['Oswald',700,'oswald'],['Bebas Neue',400,'bebas-neue'],['Fjalla One',400,'fjalla-one']];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:2400,height:200}});
let css='';for(const [f,w,d] of fams){const file=`node_modules/@fontsource/${d}/files/${d}-latin-${w}-normal.woff2`;if(!fs.existsSync(file)){console.log('missing',file);continue}css+=`@font-face{font-family:'${f}';font-weight:${w};src:url(data:font/woff2;base64,${fs.readFileSync(file).toString('base64')})}`}
await p.setContent(`<style>${css}body{margin:0;background:#000}</style><div id=t></div>`);
for(const [f,w] of fams){for(const txt of ['OPUS 5.5 COOKED','COMMENT "CLAUDE" FOR FULL GUIDE']){
 await p.evaluate(([f,w,txt])=>{document.getElementById('t').innerHTML=`<span style="font-family:'${f}';font-weight:${w};font-size:100px;color:#fff;line-height:1.3;white-space:nowrap;padding:20px;display:inline-block">${txt}</span>`},[f,w,txt]);
 await document_ready(p);
 await p.screenshot({path:`work/fm_${f.replace(/ /g,'')}_${w}_${txt.length}.png`});}}
await b.close()})();
async function document_ready(p){await p.evaluate(()=>document.fonts.ready)}
