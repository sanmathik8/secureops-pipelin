from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge
from trivy_metrics import get_vulnerability_counts
import requests
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)

vuln_high = Gauge('vulnerability_high_count', 'HIGH vulnerabilities')
vuln_critical = Gauge('vulnerability_critical_count', 'CRITICAL vulnerabilities')
security_score = Gauge('security_score', 'Security score 0-100')

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
    high, critical = get_vulnerability_counts()
    suggestions = []
    if critical > 0:
        suggestions.append("Update base image immediately")
        suggestions.append("Run: trivy image --severity CRITICAL")
    if high > 0:
        suggestions.append("Update vulnerable dependencies")
        suggestions.append("Check Dockerfile for outdated packages")
    if not suggestions:
        suggestions.append("All clear!")
    return jsonify({"suggestions": suggestions})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
