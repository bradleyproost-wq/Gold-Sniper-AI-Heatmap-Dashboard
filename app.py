<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Gold Sniper AI Heatmap Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="stylesheet" href="/static/style.css" />
</head>
<body>
  <div class="app">
    <header class="topbar">
      <div class="brand"><span class="crosshair">◎</span> GOLD SNIPER <b>AI</b></div>
      <select id="symbol"><option>XAUUSD</option><option>GC Futures</option><option>BTCUSDT</option></select>
      <nav><button class="active">M1</button><button>M5</button><button>M15</button><button>M30</button><button>H1</button><button>H4</button><button>D1</button></nav>
      <div class="topinfo"><span class="dot"></span> Server: <b id="server">Singapore (SG)</b></div>
      <div class="topinfo">Latency: <b class="green" id="latency">18ms</b></div>
      <div class="topinfo" id="clock">09:40:21 (UTC+7)</div>
    </header>

    <main class="grid">
      <aside class="left">
        <div class="card signal"><small>AI SIGNAL</small><h1 id="signal">BUY</h1><div class="arrow">↑</div></div>
        <div class="card"><small>CONFIDENCE</small><h2 id="confidence">85%</h2><div class="bar"><i id="confbar"></i></div></div>
        <div class="card"><small>REASON</small><ul id="reason"></ul></div>
        <div class="card"><small>AI SCORE</small><h2><span id="score">85</span> / 100</h2><div class="bar"><i id="scorebar"></i></div></div>
        <div class="card"><small>MARKET BIAS</small><h2 class="green" id="bias">BULLISH 🐂</h2></div>
        <div class="card"><small>VOLATILITY</small><h3 class="yellow" id="volatility">MEDIUM</h3></div>
        <div class="card"><small>SPREAD</small><h2 id="spread">0.28</h2></div>
        <div class="card"><small>CONNECTION</small><p>OKX WebSocket <span class="dot right"></span><br>Connected</p></div>
      </aside>

      <section class="center">
        <div class="chart-card">
          <div class="chart-head">
            <div><b id="chart-symbol">XAUUSD</b> ▾ · <b>M1</b></div>
            <div class="ohlc">O <span id="o"></span> H <span id="h"></span> L <span id="l"></span> C <span id="c"></span> <b class="green">+0.23 (+0.01%)</b></div>
          </div>
          <canvas id="mainChart"></canvas>
        </div>

        <div class="bottom-grid">
          <div class="card big"><small>LIQUIDITY HEATMAP (3D)</small><canvas id="miniHeat"></canvas></div>
          <div class="card big"><small>CUMULATIVE DELTA</small><h2 class="green" id="delta">+2,845</h2><canvas id="deltaChart"></canvas></div>
          <div class="card big"><small>VOLUME PROFILE</small><canvas id="profileChart"></canvas></div>
        </div>
      </section>

      <aside class="right-panel">
        <div class="card orderbook">
          <div class="tabs"><b>ORDER BOOK (OKX)</b><span>DEPTH</span><span class="active">DOM</span></div>
          <table><thead><tr><th>Price</th><th>Size</th><th>Bid</th><th>Ask</th></tr></thead><tbody id="book"></tbody></table>
          <div class="book-stats"><div>Imbalance<br><b class="green" id="imbalance">+65%</b></div><div>Buy Pressure<br><b class="green">STRONG</b></div><div>Liquidity<br><b class="green">HIGH</b></div></div>
        </div>
        <div class="row2">
          <div class="card trades"><small>TRADES FLOW <b class="green" id="delta2"></b></small><table><tbody id="trades"></tbody></table></div>
          <div class="card"><small>AI LIQUIDITY MAP</small>
            <div class="zone green-border"><small>Nearest Buy Wall</small><b id="buywall"></b><br><span>Strength: STRONG</span></div>
            <div class="zone red-border"><small>Nearest Sell Wall</small><b id="sellwall"></b><br><span>Strength: MEDIUM</span></div>
            <div class="zone blue-border"><small>Liquidity Sweep Zone</small><b id="sweep"></b><br><span>Status: CLEAN</span></div>
            <div class="zone yellow-border"><small>Fake Breakout</small><b id="fake">FALSE</b><br><span>Status: FILTER ACTIVE</span></div>
          </div>
        </div>
      </aside>
    </main>

    <footer>
      <div><small>ACCOUNT</small><b>GoldSniper-MT4</b></div>
      <div><small>BALANCE</small><b>10,254.62 USD</b></div>
      <div><small>EQUITY</small><b>10,254.62 USD</b></div>
      <div><small>FREE MARGIN</small><b>9,782.11 USD</b></div>
      <div><small>RISK</small><b>1.00%</b></div>
      <div><small>LOT SIZE</small><b>0.10</b></div>
      <button class="auto">AUTO TRADING <b>ON ●</b></button>
      <button>PENDING ORDERS (2)</button>
      <button>POSITIONS (1)</button>
    </footer>
  </div>
  <script src="/static/app.js"></script>
</body>
</html>