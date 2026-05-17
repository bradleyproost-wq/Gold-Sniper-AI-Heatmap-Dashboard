const $ = id => document.getElementById(id);
const main = $("mainChart"), mh = $("miniHeat"), dc = $("deltaChart"), pc = $("profileChart");
const ctx = main.getContext("2d"), mhx = mh.getContext("2d"), dcx = dc.getContext("2d"), pcx = pc.getContext("2d");

function fit(c){const r=c.getBoundingClientRect(); c.width=r.width*devicePixelRatio; c.height=r.height*devicePixelRatio; c.getContext("2d").setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0)}
function colorHeat(v){ if(v>80)return "rgba(255,56,31,.72)"; if(v>58)return "rgba(255,150,0,.60)"; if(v>38)return "rgba(255,230,40,.45)"; if(v>18)return "rgba(35,150,255,.28)"; return "rgba(15,55,100,.18)" }

function drawMain(data){
  fit(main); const w=main.clientWidth,h=main.clientHeight; ctx.clearRect(0,0,w,h);
  ctx.fillStyle="#06101a"; ctx.fillRect(0,0,w,h);
  for(let i=0;i<9;i++){ctx.strokeStyle="rgba(255,255,255,.045)";ctx.beginPath();ctx.moveTo(0,i*h/9);ctx.lineTo(w,i*h/9);ctx.stroke()}
  const cs=data.candles, prices=cs.flatMap(x=>[x.h,x.l]), min=Math.min(...prices)-.4,max=Math.max(...prices)+.4;
  const y=p=>h-35-(p-min)/(max-min)*(h-70), x=i=>45+i*(w-95)/cs.length;
  data.heatmap_levels.forEach(l=>{
    const yy=y(l.price), grd=ctx.createLinearGradient(0,0,w,0);
    grd.addColorStop(0,"rgba(0,0,0,0)"); grd.addColorStop(.25,colorHeat(l.strength)); grd.addColorStop(.82,colorHeat(l.strength)); grd.addColorStop(1,"rgba(0,0,0,0)");
    ctx.fillStyle=grd; ctx.fillRect(45,yy-8,w-100,16);
  });
  cs.forEach((c,i)=>{
    const xx=x(i), up=c.c>=c.o; ctx.strokeStyle=up?"#22e27a":"#ff4c5a"; ctx.fillStyle=ctx.strokeStyle;
    ctx.beginPath();ctx.moveTo(xx,y(c.h));ctx.lineTo(xx,y(c.l));ctx.stroke();
    const top=y(Math.max(c.o,c.c)), bot=y(Math.min(c.o,c.c)); ctx.fillRect(xx-3,top,6,Math.max(2,bot-top));
    ctx.fillStyle=up?"rgba(34,226,122,.45)":"rgba(255,76,90,.45)"; ctx.fillRect(xx-3,h-18-c.v/2,6,c.v/2);
  });
  const last=cs[cs.length-1].c; ctx.strokeStyle="rgba(80,255,145,.7)";ctx.setLineDash([2,2]);ctx.beginPath();ctx.moveTo(45,y(last));ctx.lineTo(w-45,y(last));ctx.stroke();ctx.setLineDash([]);
  ctx.fillStyle="#39d970";ctx.fillRect(w-75,y(last)-13,70,25);ctx.fillStyle="#001006";ctx.font="12px Arial";ctx.fillText(last.toFixed(2),w-68,y(last)+4);
  ctx.fillStyle="#ff4545";ctx.font="bold 12px Arial";ctx.fillText("SELL LIQUIDITY ↓",w-195,y(max-.5));
  ctx.fillStyle="#36e778";ctx.fillText("BUY LIQUIDITY ↑",w-195,y(min+.6));
}

function drawMini(data){
  fit(mh); const w=mh.clientWidth,h=mh.clientHeight; mhx.clearRect(0,0,w,h);
  for(let x=0;x<w;x+=8){for(let y=0;y<h;y+=8){const v=50+40*Math.sin(x/45)+25*Math.cos(y/30)+Math.random()*30;mhx.fillStyle=colorHeat(v);mhx.fillRect(x,y,8,8)}}
  mhx.fillStyle="#cbd6e5";mhx.font="12px Arial";mhx.fillText("High",w-45,20);mhx.fillText("Low",w-40,h-15)
}
function drawDelta(data){fit(dc);const w=dc.clientWidth,h=dc.clientHeight;dcx.clearRect(0,0,w,h);dcx.strokeStyle="#233044";for(let i=0;i<5;i++){dcx.beginPath();dcx.moveTo(0,i*h/5);dcx.lineTo(w,i*h/5);dcx.stroke()}let y=h/2;dcx.beginPath();for(let x=0;x<w;x+=8){y+=Math.random()*22-8; y=Math.max(20,Math.min(h-20,y)); if(x===0)dcx.moveTo(x,y); else dcx.lineTo(x,y)}dcx.strokeStyle="#3eea75";dcx.lineWidth=2;dcx.stroke()}
function drawProfile(){fit(pc);const w=pc.clientWidth,h=pc.clientHeight;pcx.clearRect(0,0,w,h);for(let i=0;i<32;i++){let len=20+Math.random()*w*.8;pcx.fillStyle=i===16?"#ffce32":"rgba(113,151,190,.55)";pcx.fillRect(10,i*h/34+8,len,5)}pcx.fillStyle="#ffce32";pcx.font="12px Arial";pcx.fillText("POC 2467.20",w-110,h/2+5)}

function render(data){
  $("signal").textContent=data.signal; $("score").textContent=data.score; $("confidence").textContent=data.confidence+"%"; $("bias").textContent=data.market_bias+(data.market_bias==="BULLISH"?" 🐂":" 🐻");
  $("volatility").textContent=data.volatility; $("spread").textContent=data.spread; $("latency").textContent=data.latency_ms+"ms"; $("server").textContent=data.server;
  $("scorebar").style.width=data.score+"%"; $("confbar").style.width=data.confidence+"%"; $("chart-symbol").textContent=data.symbol;
  const c=data.candles.at(-1); $("o").textContent=c.o; $("h").textContent=c.h; $("l").textContent=c.l; $("c").textContent=c.c;
  $("reason").innerHTML=data.reason.map(r=>`<li>${r}</li>`).join("");
  $("delta").textContent="+"+data.delta.toLocaleString(); $("delta2").textContent="Delta: +"+data.delta.toLocaleString(); $("imbalance").textContent="+"+data.imbalance+"%";
  $("buywall").textContent=data.buy_wall; $("sellwall").textContent=data.sell_wall; $("sweep").textContent=data.sweep_zone; $("fake").textContent=String(data.fake_breakout).toUpperCase();
  $("book").innerHTML=data.orderbook.asks.map(a=>`<tr><td>${a.price}</td><td>${a.size}</td><td></td><td class="red">████</td></tr>`).join("")+
    `<tr><td class="green">${data.price}</td><td></td><td colspan="2" class="green">${data.price} ▲ 0.01%</td></tr>`+
    data.orderbook.bids.map(b=>`<tr><td>${b.price}</td><td>${b.size}</td><td class="green">█████</td><td></td></tr>`).join("");
  $("trades").innerHTML=data.trades.map(t=>`<tr><td>${t.time}</td><td>${t.price}</td><td>${t.size}</td><td class="${t.side==='Buy'?'green':'red'}">${t.side}</td></tr>`).join("");
  drawMain(data); drawMini(data); drawDelta(data); drawProfile();
}
async function tick(){try{const r=await fetch("/api/state");render(await r.json())}catch(e){console.log(e)}}
setInterval(()=>{$("clock").textContent=new Date().toLocaleTimeString("en-GB")+" (UTC+7)"},1000)
tick(); setInterval(tick,1800); addEventListener("resize",tick);
