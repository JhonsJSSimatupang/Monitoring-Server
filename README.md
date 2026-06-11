# Server Monitoring Stack



## Overview

Server Monitoring Stack adalah implementasi sistem monitoring server berbasis container yang dirancang untuk melakukan observability terhadap aplikasi, container, dan resource sistem secara real-time.

Proyek ini mengintegrasikan beberapa teknologi monitoring modern yang umum digunakan pada lingkungan DevOps dan Administrasi Server, yaitu:

* Prometheus sebagai metrics collector
* Grafana sebagai visualisasi dashboard
* Flask Application sebagai target monitoring
* Node Exporter sebagai monitoring resource host
* cAdvisor sebagai monitoring container Docker
* Alertmanager sebagai sistem notifikasi dan alerting

Implementasi dilakukan menggunakan Docker Compose sehingga seluruh layanan dapat dijalankan secara otomatis dan terintegrasi dalam satu environment.

---

#  Project Objectives

* Menerapkan deployment multi-container menggunakan Docker Compose
* Mengimplementasikan monitoring server secara real-time
* Mengumpulkan metrics aplikasi dan sistem
* Membangun dashboard visualisasi profesional
* Mengimplementasikan alerting system
* Mendokumentasikan proses administrasi server secara lengkap

---

#  System Architecture
![Architecture](architecture.png)

#  Features

## Application Monitoring

* Total HTTP Requests
* Active Users Monitoring
* Endpoint Latency Tracking
* Error Rate Monitoring
* Response Time Histogram

## Infrastructure Monitoring

* CPU Usage
* Memory Utilization
* Disk Usage
* Disk I/O
* Network Traffic
* System Load

## Container Monitoring

* Container CPU Usage
* Container Memory Usage
* Container Network Usage
* Container Health Status

## Alerting

* High CPU Usage Alert
* High Memory Usage Alert
* Service Down Alert
* Application Error Alert

---

#  Technology Stack

| Component            | Technology     |
| -------------------- | -------------- |
| Backend Application  | Flask          |
| Metrics Collection   | Prometheus     |
| Dashboard            | Grafana        |
| Host Monitoring      | Node Exporter  |
| Container Monitoring | cAdvisor       |
| Alert Management     | Alertmanager   |
| Containerization     | Docker         |
| Orchestration        | Docker Compose |

---

# 📂 Project Structure

```bash
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

#  Quick Start

## Prerequisites

Pastikan perangkat telah memiliki:

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

## Build & Deploy

```bash
docker compose up -d --build
```

---

## Verify Containers

```bash
docker compose ps
```

Output yang diharapkan:

```bash
flask-app       running
prometheus      running
grafana         running
node-exporter   running
cadvisor        running
alertmanager    running
```

---

#  Service Access

| Service           | URL                   |
| ----------------- | --------------------- |
| Flask Application | http://localhost:5000 |
| Grafana Dashboard | http://localhost:3000 |
| Prometheus        | http://localhost:9090 |
| Alertmanager      | http://localhost:9093 |
| Node Exporter     | http://localhost:9100 |
| cAdvisor          | http://localhost:8080 |

---

# Metrics Collected

## Custom Flask Metrics

```text
flask_request_count_total
flask_request_latency_seconds
flask_active_users
flask_error_count_total
```

## Node Exporter Metrics

```text
CPU Usage
Memory Usage
Disk Usage
Disk I/O
Network Throughput
System Load
```

## cAdvisor Metrics

```text
Container CPU
Container Memory
Container Network
Container Filesystem
```

---

#  Performance Testing

Generate traffic untuk simulasi beban sistem:

```bash
bash scripts/load-test.sh 120
```

Script akan menghasilkan request selama 120 detik sehingga dashboard Grafana dapat menampilkan perubahan metrics secara real-time.

---

# Security Configuration

Implementasi keamanan yang digunakan:

* Grafana Authentication Enabled
* User Registration Disabled
* Isolated Docker Network
* Restart Policy Enabled
* Internal Service Communication
* Least Exposure Principle

```yaml
GF_USERS_ALLOW_SIGN_UP=false
restart: unless-stopped
```

---

# Monitoring Dashboard

Dashboard Grafana menampilkan:

* CPU Usage Overview
* Memory Utilization
* Network Traffic
* HTTP Request Rate
* Error Monitoring
* Response Time Analysis
* Container Resource Usage

Dashboard diperbarui secara otomatis berdasarkan data yang dikumpulkan Prometheus.

---

#  Troubleshooting

### Container Tidak Berjalan

```bash
docker compose logs
```

### Cek Status Semua Service

```bash
docker compose ps
```

### Restart Service

```bash
docker compose restart
```

### Rebuild Project

```bash
docker compose down

docker compose up -d --build
```

---

#  Cleanup

Stop seluruh service:

```bash
docker compose down
```

Hapus seluruh data monitoring:

```bash
docker compose down -v
```

---

#  Learning Outcomes

Melalui proyek ini berhasil diimplementasikan:

✅ Administrasi Server

✅ Multi-Container Deployment

✅ Monitoring Infrastructure

✅ Monitoring Application

✅ Docker Networking

✅ Alerting System

✅ Troubleshooting Service

✅ Dokumentasi Sistem

---
