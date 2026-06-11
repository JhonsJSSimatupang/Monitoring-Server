# Server Monitoring Stack


# 📖 Gambaran Umum

Server Monitoring Stack merupakan implementasi sistem monitoring server berbasis container yang dirancang untuk melakukan observasi (observability) terhadap aplikasi, container Docker, dan sumber daya sistem secara real-time.

Proyek ini mengintegrasikan beberapa teknologi monitoring modern yang umum digunakan pada lingkungan DevOps dan Administrasi Server, yaitu:

* Prometheus sebagai pengumpul dan penyimpan metrik.
* Grafana sebagai dashboard visualisasi data.
* Flask sebagai aplikasi target yang dimonitor.
* Node Exporter sebagai pengumpul metrik sumber daya host.
* cAdvisor sebagai pengumpul metrik container Docker.
* Alertmanager sebagai pengelola notifikasi dan peringatan sistem.

Implementasi dilakukan menggunakan Docker Compose sehingga seluruh layanan dapat dijalankan secara otomatis dan terintegrasi dalam satu lingkungan kerja.

---

# 🎯 Tujuan Proyek

* Menerapkan deployment multi-container menggunakan Docker Compose.
* Mengimplementasikan monitoring server secara real-time.
* Mengumpulkan metrik aplikasi dan sistem.
* Membangun dashboard visualisasi yang informatif.
* Mengimplementasikan sistem alerting sederhana.
* Mendokumentasikan proses administrasi server secara lengkap.

---

# 🏗️ Arsitektur Sistem

```text
┌─────────────────────────────┐
│          Browser            │
└─────────────┬───────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
    ▼                   ▼

Grafana            Flask Web App
:3000                 :5000

    ▲                   │
    │                   │
    │                   ▼

┌─────────────────────────────┐
│        Prometheus           │
│           :9090             │
└─────────────┬───────────────┘
              │
      ┌───────┼────────┐
      │       │        │
      ▼       ▼        ▼

Node Exporter  cAdvisor  Flask Metrics
:9100          :8080     /metrics

              │
              ▼

        Alertmanager
            :9093
```

---

# 🔥 Fitur Utama

## Monitoring Aplikasi

* Total permintaan HTTP (HTTP Request)
* Monitoring pengguna aktif
* Monitoring latensi endpoint
* Monitoring tingkat kesalahan (error rate)
* Analisis waktu respons aplikasi

## Monitoring Infrastruktur

* Penggunaan CPU
* Penggunaan Memori
* Penggunaan Disk
* Aktivitas Input/Output Disk
* Trafik Jaringan
* Beban Sistem (System Load)

## Monitoring Container

* Penggunaan CPU setiap container
* Penggunaan memori setiap container
* Penggunaan jaringan setiap container
* Status kesehatan container

## Sistem Peringatan (Alerting)

* Peringatan penggunaan CPU tinggi
* Peringatan penggunaan memori tinggi
* Peringatan layanan tidak aktif
* Peringatan kesalahan aplikasi

---

# 📦 Teknologi yang Digunakan

| Komponen             | Teknologi      |
| -------------------- | -------------- |
| Aplikasi Backend     | Flask          |
| Pengumpulan Metrik   | Prometheus     |
| Dashboard Monitoring | Grafana        |
| Monitoring Host      | Node Exporter  |
| Monitoring Container | cAdvisor       |
| Manajemen Alert      | Alertmanager   |
| Containerisasi       | Docker         |
| Orkestrasi           | Docker Compose |

---

# 📂 Struktur Proyek

```text
server-monitoring/
│
├── docker-compose.yml
│
├── flask-app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── prometheus/
│   ├── prometheus.yml
│   └── alert_rules.yml
│
├── grafana/
│   └── provisioning/
│       ├── datasources/
│       │   └── prometheus.yml
│       │
│       └── dashboards/
│           └── dashboard.yml
│
├── alertmanager/
│   └── alertmanager.yml
│
└── scripts/
    └── load-test.sh
```

---

# 🚀 Cara Menjalankan

## Persyaratan

Pastikan perangkat telah terpasang:

* Docker Desktop
* Docker Compose
* Git

Verifikasi instalasi:

```bash
docker --version
docker compose version
git --version
```

---

## Clone Repository

```bash
git clone https://github.com/<username>/server-monitoring.git

cd server-monitoring
```

---

## Build dan Menjalankan Sistem

```bash
docker compose up -d --build
```

---

## Memeriksa Status Container

```bash
docker compose ps
```

---

# 🌐 Akses Layanan

| Layanan           | URL                   |
| ----------------- | --------------------- |
| Flask Application | http://localhost:5000 |
| Grafana Dashboard | http://localhost:3000 |
| Prometheus        | http://localhost:9090 |
| Alertmanager      | http://localhost:9093 |
| Node Exporter     | http://localhost:9100 |
| cAdvisor          | http://localhost:8080 |

---

# 📊 Metrik yang Dimonitor

## Metrik Aplikasi Flask

* flask_request_count_total
* flask_request_latency_seconds
* flask_active_users
* flask_error_count_total

## Metrik Sistem (Node Exporter)

* Penggunaan CPU
* Penggunaan Memori
* Penggunaan Disk
* Aktivitas Disk I/O
* Trafik Jaringan
* Beban Sistem

## Metrik Container (cAdvisor)

* Penggunaan CPU Container
* Penggunaan Memori Container
* Penggunaan Jaringan Container
* Penggunaan Sistem Berkas Container

---

# 🧪 Pengujian Performa

Untuk mensimulasikan beban pada aplikasi:

```bash
bash scripts/load-test.sh 120
```

Script akan menghasilkan trafik selama 120 detik sehingga perubahan metrik dapat diamati secara langsung pada dashboard Grafana.

---

# 🔐 Konfigurasi Keamanan

Beberapa mekanisme keamanan yang diterapkan:

* Autentikasi Grafana diaktifkan.
* Registrasi pengguna dinonaktifkan.
* Jaringan Docker terisolasi.
* Kebijakan restart otomatis container.
* Komunikasi internal antar layanan.
* Prinsip pembatasan akses minimum (Least Privilege).

---

# 📈 Dashboard Monitoring

Dashboard Grafana menampilkan informasi:

* Penggunaan CPU
* Penggunaan Memori
* Trafik Jaringan
* Jumlah Request HTTP
* Monitoring Error
* Analisis Waktu Respons
* Penggunaan Resource Container

Semua data diperbarui secara otomatis berdasarkan metrik yang dikumpulkan oleh Prometheus.

---

# 🛠️ Troubleshooting

### Melihat Log Container

```bash
docker compose logs
```

### Memeriksa Status Layanan

```bash
docker compose ps
```

### Restart Seluruh Layanan

```bash
docker compose restart
```

### Rebuild Sistem

```bash
docker compose down
docker compose up -d --build
```

---

# 🧹 Menghentikan dan Membersihkan Sistem

Menghentikan seluruh layanan:

```bash
docker compose down
```

Menghapus seluruh data monitoring:

```bash
docker compose down -v
```

---

# 🎓 Hasil Pembelajaran

Melalui proyek ini berhasil diterapkan:

✅ Administrasi Server

✅ Deployment Multi-Container

✅ Monitoring Infrastruktur

✅ Monitoring Aplikasi

✅ Docker Networking

✅ Sistem Alerting

✅ Troubleshooting Layanan

✅ Dokumentasi Sistem

---

