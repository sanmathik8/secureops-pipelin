from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge
import requests
import json
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)

vuln_high = Gauge('vulnerability_high_count', 'HIGH vulnerabilities')
vuln_critical = Gauge('vulnerability_critical_count', 'CRITICAL vulnerabilities')
security_score = Gauge('security_score', 'Security score 0-100')

def load_report():
    report_file = "/app/trivy-report.json"
    if not os.path.exists(report_file):
        return []
    with open(report_file) as f:
        data = json.load(f)
    vulns = []
    for result in data.get("Results", []):
        for vuln in result.get("Vulnerabilities", []):
            vulns.append(vuln)
    return vulns

def get_vulnerability_counts():
    high = critical = 0
    for vuln in load_report():
        if vuln.get("Severity") == "HIGH":
            high += 1
        elif vuln.get("Severity") == "CRITICAL":
            critical += 1
    return high, critical

def calculate_grade(high, critical):
    if critical > 0: return "D", 25
    elif high > 5: return "C", 50
    elif high > 0: return "B", 75
    else: return "A", 100

def notify_n8n(payload):
    url = os.getenv("N8N_WEBHOOK_URL", "")
    if url:
        requests.post(url, json=payload)

@app.route("/")
def home():
    return jsonify({"status": "running"})

@app.route("/health")
def health():
    return jsonify({"healthy": True})

@app.route("/vuln-status")
def vuln_status():
    high, critical = get_vulnerability_counts()
    grade, score = calculate_grade(high, critical)
    vuln_high.set(high)
    vuln_critical.set(critical)
    security_score.set(score)
    payload = {"high": high, "critical": critical, "grade": grade, "score": score}
    notify_n8n(payload)
    return jsonify(payload)

@app.route("/fix-suggestions")
def fix_suggestions():
    vulns = load_report()
    suggestions = []
    for vuln in vulns:
        severity = vuln.get("Severity", "")
        if severity in ["CRITICAL", "HIGH"]:
            pkg = vuln.get("PkgName", "unknown")
            cve = vuln.get("VulnerabilityID", "N/A")
            installed = vuln.get("InstalledVersion", "?")
            fixed = vuln.get("FixedVersion", "No fix available")
            suggestions.append(
                f"{severity} | {cve} | {pkg} {installed} → {fixed}"
            )
    if not suggestions:
        suggestions.append("All clear! No critical or high vulnerabilities.")
    return jsonify({"suggestions": suggestions})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
