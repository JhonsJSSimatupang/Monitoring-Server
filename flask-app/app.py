from flask import Flask, jsonify, render_template_string
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import randomfrom flask import Flask, jsonify, render_template_string
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

# ── Prometheus Metrics ──────────────────────────────────────────
REQUEST_COUNT = Counter(
    'flask_request_count_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'flask_request_latency_seconds',
    'HTTP request latency',
    ['endpoint']
)

ACTIVE_USERS = Gauge(
    'flask_active_users',
    'Simulated active users on the app'
)

ERROR_COUNT = Counter(
    'flask_error_count_total',
    'Total errors',
    ['endpoint']
)

APP_START_TIME = time.time()

# ── Middleware ──────────────────────────────────────────────────
@app.before_request
def start_timer():
    from flask import g
    g.start_time = time.time()

@app.after_request
def record_metrics(response):
    from flask import g, request
    latency = time.time() - g.start_time
    if request.path != '/metrics':
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.path,
            status=response.status_code
        ).inc()
        REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
    return response

# ── HTML Template ───────────────────────────────────────────────
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Sistem Monitoring</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"/>
  <style>
    :root {
      --bg:       #080c14;
      --surface:  #0d1424;
      --border:   #1a2540;
      --accent:   #00d4ff;
      --accent2:  #7c3aed;
      --green:    #00e676;
      --red:      #ff3d71;
      --yellow:   #ffd740;
      --text:     #e2e8f0;
      --muted:    #64748b;
      --glow:     0 0 20px rgba(0,212,255,.15);
    }
    * { margin:0; padding:0; box-sizing:border-box; }
    body {
      font-family: 'Space Grotesk', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* ── Grid bg ── */
    body::before {
      content:'';
      position:fixed; inset:0;
      background-image:
        linear-gradient(rgba(0,212,255,.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,.03) 1px, transparent 1px);
      background-size: 40px 40px;
      pointer-events:none;
      z-index:0;
    }

    .wrap { position:relative; z-index:1; max-width:1100px; margin:0 auto; padding:32px 24px; }

    /* ── Header ── */
    header {
      display:flex; align-items:center; justify-content:space-between;
      margin-bottom:40px; padding-bottom:24px;
      border-bottom:1px solid var(--border);
    }
    .logo { display:flex; align-items:center; gap:12px; }
    .logo-icon {
      width:40px; height:40px; border-radius:10px;
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      display:flex; align-items:center; justify-content:center;
      font-size:18px; box-shadow: var(--glow);
    }
    .logo-text { font-size:22px; font-weight:700; letter-spacing:-.5px; }
    .logo-text span { color:var(--accent); }
    .badge {
      font-family:'JetBrains Mono', monospace;
      font-size:11px; padding:4px 10px; border-radius:20px;
      background:rgba(0,230,118,.1); color:var(--green);
      border:1px solid rgba(0,230,118,.3);
      display:flex; align-items:center; gap:6px;
    }
    .badge::before {
      content:''; width:6px; height:6px; border-radius:50%;
      background:var(--green);
      animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse {
      0%,100%{ opacity:1; transform:scale(1); }
      50%{ opacity:.4; transform:scale(.8); }
    }

    /* ── Stats grid ── */
    .stats { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:32px; }
    @media(max-width:700px){ .stats{ grid-template-columns:repeat(2,1fr); } }
    .stat-card {
      background:var(--surface); border:1px solid var(--border);
      border-radius:14px; padding:20px;
      transition: border-color .2s, box-shadow .2s;
    }
    .stat-card:hover { border-color:var(--accent); box-shadow:var(--glow); }
    .stat-label {
      font-size:11px; font-weight:600; letter-spacing:.08em;
      text-transform:uppercase; color:var(--muted); margin-bottom:10px;
    }
    .stat-value {
      font-family:'JetBrains Mono', monospace;
      font-size:28px; font-weight:600; line-height:1;
    }
    .stat-sub { font-size:12px; color:var(--muted); margin-top:6px; }
    .c-cyan   { color:var(--accent); }
    .c-green  { color:var(--green); }
    .c-purple { color:#a78bfa; }
    .c-yellow { color:var(--yellow); }

    /* ── Two-col layout ── */
    .grid2 { display:grid; grid-template-columns:1.4fr 1fr; gap:20px; margin-bottom:24px; }
    @media(max-width:800px){ .grid2{ grid-template-columns:1fr; } }

    /* ── Panel ── */
    .panel {
      background:var(--surface); border:1px solid var(--border);
      border-radius:14px; padding:24px;
    }
    .panel-title {
      font-size:13px; font-weight:600; letter-spacing:.06em;
      text-transform:uppercase; color:var(--muted);
      margin-bottom:18px; display:flex; align-items:center; gap:8px;
    }
    .panel-title .dot {
      width:8px; height:8px; border-radius:50%;
    }

    /* ── Endpoint buttons ── */
    .endpoints { display:flex; flex-direction:column; gap:10px; }
    .ep-btn {
      display:flex; align-items:center; justify-content:space-between;
      padding:12px 16px; border-radius:10px;
      background:rgba(255,255,255,.03); border:1px solid var(--border);
      color:var(--text); text-decoration:none; cursor:pointer;
      transition: all .2s; font-family:inherit; font-size:14px; width:100%;
    }
    .ep-btn:hover { background:rgba(0,212,255,.07); border-color:var(--accent); transform:translateX(4px); }
    .ep-name { display:flex; align-items:center; gap:10px; font-weight:500; }
    .ep-icon { font-size:16px; }
    .ep-tag {
      font-family:'JetBrains Mono', monospace;
      font-size:10px; padding:2px 8px; border-radius:4px;
    }
    .tag-get  { background:rgba(0,212,255,.12); color:var(--accent); }
    .tag-ok   { background:rgba(0,230,118,.12); color:var(--green); }
    .tag-slow { background:rgba(255,215,64,.12); color:var(--yellow); }
    .tag-err  { background:rgba(255,61,113,.12); color:var(--red); }

    /* ── Activity log ── */
    .log-list { display:flex; flex-direction:column; gap:8px; max-height:220px; overflow-y:auto; }
    .log-list::-webkit-scrollbar { width:4px; }
    .log-list::-webkit-scrollbar-track { background:transparent; }
    .log-list::-webkit-scrollbar-thumb { background:var(--border); border-radius:2px; }
    .log-item {
      display:flex; align-items:center; gap:10px;
      font-family:'JetBrains Mono', monospace; font-size:12px; color:var(--muted);
      padding:6px 10px; border-radius:6px; background:rgba(255,255,255,.02);
      animation: fadeIn .3s ease;
    }
    @keyframes fadeIn { from{ opacity:0; transform:translateY(-4px); } to{ opacity:1; transform:translateY(0); } }
    .log-status { font-weight:600; min-width:32px; }
    .s-200 { color:var(--green); }
    .s-500 { color:var(--red); }
    .s-slow{ color:var(--yellow); }

    /* ── Links row ── */
    .links { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; }
    .link-card {
      display:flex; flex-direction:column; align-items:center; justify-content:center;
      gap:8px; padding:18px 12px; border-radius:12px;
      background:rgba(255,255,255,.02); border:1px solid var(--border);
      text-decoration:none; color:var(--text);
      transition:all .2s;
    }
    .link-card:hover { border-color:var(--accent); background:rgba(0,212,255,.06); box-shadow:var(--glow); }
    .link-card .licon { font-size:24px; }
    .link-card .lname { font-size:13px; font-weight:600; }
    .link-card .lport {
      font-family:'JetBrains Mono', monospace;
      font-size:11px; color:var(--muted);
    }

    /* ── Response box ── */
    .response-box {
      margin-top:14px; padding:14px; border-radius:8px;
      background:#060a10; border:1px solid var(--border);
      font-family:'JetBrains Mono', monospace; font-size:12px;
      color:#94a3b8; min-height:48px; line-height:1.6;
      white-space:pre-wrap; word-break:break-all;
      display:none;
    }
    .response-box.show { display:block; animation: fadeIn .2s ease; }

    footer {
      margin-top:40px; padding-top:20px; border-top:1px solid var(--border);
      text-align:center; font-size:12px; color:var(--muted);
    }
  </style>
</head>
<body>
<div class="wrap">

  <!-- Header -->
  <header>
    <div class="logo">
      <div class="logo-icon">⚡</div>
      <div class="logo-text">Sistem <span>Monitoring</span></div>
    </div>
    <div class="badge">SYSTEM ONLINE</div>
  </header>

  <!-- Stats -->
  <div class="stats">
    <div class="stat-card">
      <div class="stat-label">Total Requests</div>
      <div class="stat-value c-cyan" id="total-req">—</div>
      <div class="stat-sub">sejak server start</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Active Users</div>
      <div class="stat-value c-green" id="active-users">—</div>
      <div class="stat-sub">simulasi realtime</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Uptime</div>
      <div class="stat-value c-purple" id="uptime">—</div>
      <div class="stat-sub">server berjalan</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Error Rate</div>
      <div class="stat-value c-yellow" id="error-rate">—</div>
      <div class="stat-sub">dari total request</div>
    </div>
  </div>

  <!-- Main grid -->
  <div class="grid2">

    <!-- Endpoints -->
    <div class="panel">
      <div class="panel-title">
        <span class="dot" style="background:var(--accent)"></span>
        API Endpoints
      </div>
      <div class="endpoints">
        <button class="ep-btn" onclick="hit('/api/data', 'data')">
          <span class="ep-name"><span class="ep-icon">📊</span> api/data</span>
          <span class="ep-tag tag-get">GET</span>
        </button>
        <button class="ep-btn" onclick="hit('/api/slow', 'slow')">
          <span class="ep-name"><span class="ep-icon">🐢</span> api/slow</span>
          <span class="ep-tag tag-slow">SLOW</span>
        </button>
        <button class="ep-btn" onclick="hit('/api/error', 'err')">
          <span class="ep-name"><span class="ep-icon">💥</span> api/error</span>
          <span class="ep-tag tag-err">50% ERR</span>
        </button>
        <button class="ep-btn" onclick="hit('/health', 'health')">
          <span class="ep-name"><span class="ep-icon">❤️</span> health</span>
          <span class="ep-tag tag-ok">OK</span>
        </button>
        <a class="ep-btn" href="/metrics" target="_blank">
          <span class="ep-name"><span class="ep-icon">📈</span> metrics</span>
          <span class="ep-tag tag-get">PROM</span>
        </a>
      </div>
      <div class="response-box" id="resp-box">klik endpoint untuk lihat response...</div>
    </div>

    <!-- Log -->
    <div class="panel">
      <div class="panel-title">
        <span class="dot" style="background:var(--green)"></span>
        Activity Log
      </div>
      <div class="log-list" id="log-list">
        <div class="log-item"><span class="log-status s-200">—</span><span>Menunggu request...</span></div>
      </div>
    </div>

  </div>

  <!-- External links -->
  <div class="links">
    <a class="link-card" href="http://localhost:3000" target="_blank">
      <span class="licon">📊</span>
      <span class="lname">Grafana</span>
      <span class="lport">:3000</span>
    </a>
    <a class="link-card" href="http://localhost:9090" target="_blank">
      <span class="licon">🔥</span>
      <span class="lname">Prometheus</span>
      <span class="lport">:9090</span>
    </a>
    <a class="link-card" href="http://localhost:9093" target="_blank">
      <span class="licon">🚨</span>
      <span class="lname">Alertmanager</span>
      <span class="lport">:9093</span>
    </a>
  </div>

  <footer>SysMon · Flask + Prometheus + Grafana · Universitas Brawijaya</footer>
</div>

<script>
  let totalReq = 0, totalErr = 0;
  const startTime = Date.now();
  const logList = document.getElementById('log-list');
  const respBox = document.getElementById('resp-box');

  function addLog(path, status, ms) {
    const cls = status >= 500 ? 's-500' : status >= 400 ? 's-slow' : 's-200';
    const tag = status >= 500 ? 's-500' : 's-200';
    const item = document.createElement('div');
    item.className = 'log-item';
    const t = new Date().toLocaleTimeString('id-ID', {hour:'2-digit',minute:'2-digit',second:'2-digit'});
    item.innerHTML = `<span class="log-status ${cls}">${status}</span><span style="flex:1">${path}</span><span style="color:#475569">${ms}ms</span><span style="color:#334155">${t}</span>`;
    logList.insertBefore(item, logList.firstChild);
    if (logList.children.length > 20) logList.removeChild(logList.lastChild);
  }

  async function hit(path, type) {
    const t0 = Date.now();
    respBox.className = 'response-box';
    respBox.textContent = '⏳ loading...';
    respBox.className = 'response-box show';
    try {
      const res = await fetch(path);
      const ms = Date.now() - t0;
      const data = await res.json();
      totalReq++;
      if (res.status >= 500) totalErr++;
      addLog(path, res.status, ms);
      respBox.textContent = JSON.stringify(data, null, 2);
      updateStats();
    } catch(e) {
      totalReq++; totalErr++;
      const ms = Date.now() - t0;
      addLog(path, 500, ms);
      respBox.textContent = '❌ ' + e.message;
      updateStats();
    }
  }

  function formatUptime(ms) {
    const s = Math.floor(ms/1000);
    if (s < 60) return s + 's';
    if (s < 3600) return Math.floor(s/60) + 'm ' + (s%60) + 's';
    return Math.floor(s/3600) + 'h ' + Math.floor((s%3600)/60) + 'm';
  }

  function updateStats() {
    document.getElementById('total-req').textContent = totalReq;
    const rate = totalReq > 0 ? ((totalErr/totalReq)*100).toFixed(1)+'%' : '0%';
    document.getElementById('error-rate').textContent = rate;
    document.getElementById('uptime').textContent = formatUptime(Date.now() - startTime);
  }

  async function fetchActiveUsers() {
    try {
      const res = await fetch('/api/data');
      const data = await res.json();
      const u = Math.floor(Math.random()*49)+1;
      document.getElementById('active-users').textContent = u;
    } catch(e){}
  }

  setInterval(() => {
    document.getElementById('uptime').textContent = formatUptime(Date.now() - startTime);
  }, 1000);

  setInterval(fetchActiveUsers, 5000);
  fetchActiveUsers();
  updateStats();
</script>
</body>
</html>
"""

@app.route('/')
def index():
    ACTIVE_USERS.set(random.randint(1, 50))
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/data')
def api_data():
    return jsonify({
        "status": "ok",
        "message": "Data dari Flask API",
        "timestamp": time.time(),
        "data": [random.randint(1, 100) for _ in range(5)]
    })

@app.route('/api/slow')
def api_slow():
    delay = random.uniform(0.5, 3.0)
    time.sleep(delay)
    return jsonify({
        "status": "ok",
        "message": f"Response setelah {delay:.2f} detik",
        "delay": delay
    })

@app.route('/api/error')
def api_error():
    if random.random() < 0.5:
        ERROR_COUNT.labels(endpoint='/api/error').inc()
        return jsonify({"status": "error", "message": "Simulated server error"}), 500
    return jsonify({"status": "ok", "message": "Berhasil (tidak error kali ini)"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "uptime": time.time() - APP_START_TIME})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

app = Flask(__name__)

# ── Prometheus Metrics ──────────────────────────────────────────
REQUEST_COUNT = Counter(
    'flask_request_count_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'flask_request_latency_seconds',
    'HTTP request latency',
    ['endpoint']
)

ACTIVE_USERS = Gauge(
    'flask_active_users',
    'Simulated active users on the app'
)

ERROR_COUNT = Counter(
    'flask_error_count_total',
    'Total errors',
    ['endpoint']
)

# ── Middleware: catat setiap request ────────────────────────────
@app.before_request
def start_timer():
    from flask import g
    g.start_time = time.time()

@app.after_request
def record_metrics(response):
    from flask import g, request
    latency = time.time() - g.start_time
    if request.path != '/metrics':
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.path,
            status=response.status_code
        ).inc()
        REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
    return response

# ── Routes ───────────────────────────────────────────────────────
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Server Monitoring Demo App</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
        .card { background: white; padding: 20px; border-radius: 8px; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        a { color: #007bff; text-decoration: none; margin-right: 15px; }
        a:hover { text-decoration: underline; }
        .status { color: green; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🖥️ Server Monitoring Demo</h1>
        <p>Flask web app yang dimonitor oleh <strong>Prometheus + Grafana</strong>.</p>
        <p>Status: <span class="status">● Running</span></p>
    </div>
    <div class="card">
        <h2>Endpoints</h2>
        <a href="/">🏠 Home</a>
        <a href="/api/data">📊 API Data</a>
        <a href="/api/slow">🐢 Slow Endpoint</a>
        <a href="/api/error">💥 Simulate Error</a>
        <a href="/metrics">📈 Metrics</a>
        <a href="/health">❤️ Health</a>
    </div>
    <div class="card">
        <p>Buka <strong>Grafana</strong> di <a href="http://localhost:3000" target="_blank">localhost:3000</a> untuk lihat dashboard monitoring.</p>
        <p>Buka <strong>Prometheus</strong> di <a href="http://localhost:9090" target="_blank">localhost:9090</a> untuk query metrics langsung.</p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    ACTIVE_USERS.set(random.randint(1, 50))
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/data')
def api_data():
    return jsonify({
        "status": "ok",
        "message": "Data dari Flask API",
        "timestamp": time.time(),
        "data": [random.randint(1, 100) for _ in range(5)]
    })

@app.route('/api/slow')
def api_slow():
    """Endpoint lambat untuk simulasi latency tinggi"""
    delay = random.uniform(0.5, 3.0)
    time.sleep(delay)
    return jsonify({
        "status": "ok",
        "message": f"Response setelah {delay:.2f} detik",
        "delay": delay
    })

@app.route('/api/error')
def api_error():
    """Endpoint yang kadang error (50% chance)"""
    if random.random() < 0.5:
        ERROR_COUNT.labels(endpoint='/api/error').inc()
        return jsonify({"status": "error", "message": "Simulated server error"}), 500
    return jsonify({"status": "ok", "message": "Berhasil (tidak error kali ini)"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "uptime": time.time()})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
