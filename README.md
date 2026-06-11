# 🖥️ Server Monitoring Stack

Proyek implementasi sistem monitoring server menggunakan **Prometheus + Grafana + Flask**, dikerjakan sebagai bagian dari tugas Unjuk Keterampilan Administrasi Server.

## 📐 Arsitektur Sistem

```
Browser
  ├── localhost:3000  →  Grafana (Dashboard Monitoring)
  ├── localhost:5000  →  Flask Web App (Target yang dimonitor)
  ├── localhost:9090  →  Prometheus (Time-series Database)
  ├── localhost:9093  →  Alertmanager
  ├── localhost:9100  →  Node Exporter (metrics sistem)
  └── localhost:8080  →  cAdvisor (metrics container)

Prometheus scrapes:
  ├── flask-app:5000/metrics   → custom app metrics
  ├── node-exporter:9100       → CPU, RAM, disk, network
  └── cadvisor:8080            → container resource usage
```

## 🧩 Komponen

| Komponen | Image | Port | Fungsi |
|---|---|---|---|
| Flask App | custom build | 5000 | Web app target monitoring |
| Prometheus | prom/prometheus | 9090 | Scrape & simpan metrics |
| Grafana | grafana/grafana | 3000 | Visualisasi dashboard |
| Node Exporter | prom/node-exporter | 9100 | Metrics resource sistem host |
| cAdvisor | gcr.io/cadvisor | 8080 | Metrics container Docker |
| Alertmanager | prom/alertmanager | 9093 | Manajemen alert |

## 🚀 Cara Menjalankan

### Prerequisites
- Docker Desktop terinstall dan berjalan
- Git

### 1. Clone repository
```bash
git clone https://github.com/<username>/server-monitoring.git
cd server-monitoring
```

### 2. Jalankan semua layanan
```bash
docker compose up -d --build
```

### 3. Cek status container
```bash
docker compose ps
```

### 4. Akses layanan
| URL | Keterangan |
|---|---|
| http://localhost:5000 | Flask Web App |
| http://localhost:3000 | Grafana (admin / admin123) |
| http://localhost:9090 | Prometheus |
| http://localhost:9093 | Alertmanager |

### 5. Generate traffic untuk demo
```bash
bash scripts/load-test.sh 120   # jalankan load test 2 menit
```

## 📊 Metrics yang Dimonitor

### Flask App Metrics (custom)
- `flask_request_count_total` — total HTTP request per endpoint & status
- `flask_request_latency_seconds` — latency per endpoint (histogram)
- `flask_active_users` — simulasi jumlah user aktif
- `flask_error_count_total` — total error yang terjadi

### System Metrics (Node Exporter)
- CPU usage per core
- Memory usage & available
- Disk I/O & usage
- Network traffic in/out

### Container Metrics (cAdvisor)
- CPU usage per container
- Memory usage per container
- Network per container

## 🔐 Keamanan

- Grafana menggunakan autentikasi username/password (non-default)
- `GF_USERS_ALLOW_SIGN_UP=false` — registrasi user dinonaktifkan
- Docker network terisolasi (`monitoring` bridge network)
- Container berjalan dengan policy `restart: unless-stopped`

## 🛑 Menghentikan & Membersihkan

```bash
# Stop semua container
docker compose down

# Stop + hapus volume (data Prometheus & Grafana)
docker compose down -v
```

## 📁 Struktur Folder

```
server-monitoring/
├── docker-compose.yml
├── flask-app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── prometheus/
│   ├── prometheus.yml
│   └── alert_rules.yml
├── grafana/
│   └── provisioning/
│       ├── datasources/
│       │   └── prometheus.yml
│       └── dashboards/
│           └── dashboard.yml
├── alertmanager/
│   └── alertmanager.yml
└── scripts/
    └── load-test.sh
```

