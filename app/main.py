from flask import Flask, jsonify
import requests
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Vulnerability metrics
vuln_high = Gauge('vulnerability_high_count', 'Number of HIGH severity vulnerabilities')
vuln_critical = Gauge('vulnerability_critical_count', 'Number of CRITICAL severity vulnerabilities')

# Set current known values from Trivy scan
vuln_high.set(26)
vuln_critical.set(5)

@app.route("/")
def home():
    return jsonify({"status": "running", "app": "SecureOps Pipeline"})

@app.route("/health")
def health():
    return jsonify({"healthy": True})

@app.route("/vuln-status")
def vuln_status():
    return jsonify({
        "high": 26,
        "critical": 5,
        "status": "vulnerable"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
