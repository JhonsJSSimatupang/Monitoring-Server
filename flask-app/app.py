from flask import Flask, jsonify, render_template_string
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
