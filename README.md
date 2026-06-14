# 🔐 SecureOps Pipeline

An end-to-end **DevSecOps automation platform** that automatically detects vulnerabilities, scans source code, performs live attack simulation, monitors security health, and alerts the team — all without manual intervention.

---

## 🏗️ Architecture

Code Push (GitHub)
↓ auto triggers
Jenkins → Build Docker Image
↓
Bandit → SAST (Python source code scan)
↓
Trivy → SCA (container vulnerability scan)
↓
Kubernetes (kind) → Deploy
↓
OWASP ZAP → DAST (live attack simulation)
↓
Prometheus → Scrape security metrics
↓
Grafana → Security dashboard
↓
n8n → Nightly scan → Auto GitHub issue

---

## 🧰 Tech Stack

| Tool | Purpose |
|------|---------|
| GitHub | Source control + issue tracking |
| Jenkins | CI/CD pipeline automation |
| Docker | Containerization |
| Kubernetes (kind) | Local cluster deployment |
| Bandit | SAST — Python source code analysis |
| Trivy | SCA — container image vulnerability scanning |
| OWASP ZAP | DAST — live web application attack simulation |
| Prometheus | Metrics collection |
| Grafana | Security dashboard |
| n8n | Workflow automation |

---

## ✨ Features

- ✅ Auto-build on every code push
- ✅ SAST scan with Bandit — catches insecure Python code patterns
- ✅ Container vulnerability scanning with Trivy (HIGH + CRITICAL)
- ✅ Auto-generated remediation suggestions via custom scripts
- ✅ Kubernetes deployment with kind cluster
- ✅ DAST scan with OWASP ZAP after every deployment
- ✅ Security headers enforced on Flask app (CSP, X-Content-Type-Options, etc.)
- ✅ Live security metrics dashboard in Grafana
- ✅ Nightly automated vulnerability scan via n8n
- ✅ Auto GitHub issue creation when critical CVEs found

---

## 🚀 Pipeline Stages

| Stage | Tool | What It Does |
|-------|------|-------------|
| Checkout | Git | Pulls latest code from GitHub |
| Build Docker Image | Docker | Builds the Flask app container |
| Bandit SAST Scan | Bandit | Scans Python source for insecure code — fails on HIGH severity |
| Security Scan | Trivy | Scans Docker image for CVEs — reports HIGH/CRITICAL |
| Generate Security Report | Python | Parses Trivy output, generates fix suggestions |
| Security Report Summary | Python | Prints CRITICAL CVEs to console |
| Load Image into Kubernetes | kind | Loads image into local cluster |
| Deploy to Kubernetes | kubectl | Applies deployment and service manifests |
| OWASP ZAP DAST Scan | ZAP | Port-forwards service and runs baseline attack scan |

---

## 🔒 Security Layers

This pipeline implements three layers of security scanning:

**1. SAST — Static Application Security Testing (Bandit)**
Scans Python source code before the image is built. Catches issues like hardcoded secrets, use of insecure functions, and SQL injection patterns. Pipeline fails if any HIGH severity issue is found.

**2. SCA — Software Composition Analysis (Trivy)**
Scans the built Docker image for known CVEs in OS packages and Python dependencies. Reports HIGH and CRITICAL vulnerabilities with fix availability and remediation suggestions.

**3. DAST — Dynamic Application Security Testing (OWASP ZAP)**
After deployment, port-forwards the live Kubernetes service and runs a baseline scan against the running app. Catches runtime issues like missing security headers, information disclosure, and misconfigured policies.

---

## 📊 Security Headers

The Flask app enforces the following security headers on every response:

| Header | Value |
|--------|-------|
| X-Content-Type-Options | nosniff |
| X-Frame-Options | DENY |
| X-XSS-Protection | 1; mode=block |
| Content-Security-Policy | default-src 'self' |
| Permissions-Policy | geolocation=(), microphone=(), camera=() |
| Cross-Origin-Resource-Policy | same-origin |

---

## 📈 Monitoring Dashboard

Grafana dashboard at http://localhost:3000 shows:

- Memory usage
- HTTP request rate
- HIGH vulnerability count (live)
- CRITICAL vulnerability count (live)
- Real-time security alerts

---

## 🛠️ Setup

Clone repo:
git clone https://github.com/sanmathik8/secureops-pipelin.git

Start monitoring stack:
docker compose up -d

Access dashboards:
Grafana:    http://localhost:3000
Prometheus: http://localhost:9090
n8n:        http://localhost:5678

Prerequisites:
- Docker Desktop (Windows)
- kind
- kubectl
- Jenkins (running as service on Windows)
- Python 3.x

---

## 🐛 Known Issues

| Issue | Status |
|-------|--------|
| perl-base CVE-2026-42496 | No fix available upstream |
| perl-base CVE-2026-8376 | No fix available upstream |

These CVEs exist in the base python:3.11-slim image and have no available patch at time of writing. Tracked and documented via auto-generated suggestions.txt.

---

## 👩‍💻 Author

Sanmathi Priya K S
Fresher — DevOps and DevSecOps
GitHub: https://github.com/sanmathik8
