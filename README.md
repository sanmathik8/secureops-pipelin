# 🔐 SecureOps Pipeline

An end-to-end **DevSecOps automation platform** that automatically detects vulnerabilities, monitors security health, and alerts the team — all without manual intervention.

## 🏗️ Architecture
Code Push (GitHub)
↓ auto triggers
Jenkins → Build + Test
↓
Docker → Package app
↓
Trivy → Scan vulnerabilities
↓
Kubernetes (kind) → Deploy
↓
Prometheus → Scrape metrics
↓
Grafana → Security dashboard
↓
n8n → Nightly scan → Auto GitHub issue

## 🧰 Tech Stack

| Tool | Purpose |
|------|---------|
| GitHub | Source control + issue tracking |
| Jenkins | CI/CD pipeline |
| Docker | Containerization |
| Kubernetes (kind) | Local cluster deployment |
| Trivy | Vulnerability scanning |
| Prometheus | Metrics collection |
| Grafana | Security dashboard |
| n8n | Workflow automation |

## ✨ Features

- ✅ Auto-build on every code push
- ✅ Docker image vulnerability scanning with Trivy
- ✅ Live security metrics dashboard in Grafana
- ✅ Nightly automated vulnerability scan via n8n
- ✅ Auto GitHub issue creation when critical CVEs found
- ✅ Kubernetes deployment with kind

## 🚀 How It Works

1. Developer pushes code to GitHub
2. Jenkins detects push within 1 minute and builds Docker image
3. Trivy scans image for HIGH/CRITICAL vulnerabilities
4. Image deployed to Kubernetes cluster
5. Prometheus scrapes vulnerability metrics from Flask app
6. Grafana displays real-time security health dashboard
7. n8n runs nightly → checks Prometheus → creates GitHub issue if vulns found

## 📊 Dashboard

- Memory usage
- HTTP request rate
- Vulnerability count (HIGH + CRITICAL)
- Real-time security alerts

## 🛠️ Setup

```bash
# Clone repo
git clone https://github.com/sanmathik8/secureops-pipelin.git

# Start monitoring stack
docker compose up -d

# Access dashboards
# Grafana: http://localhost:3000
# Prometheus: http://localhost:9090
# n8n: http://localhost:5678
