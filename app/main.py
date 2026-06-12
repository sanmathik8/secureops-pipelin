from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge
from trivy_metrics import get_vulnerability_counts

app = Flask(__name__)
metrics = PrometheusMetrics(app)

vuln_high = Gauge(
    'vulnerability_high_count',
    'Number of HIGH severity vulnerabilities'
)

vuln_critical = Gauge(
    'vulnerability_critical_count',
    'Number of CRITICAL severity vulnerabilities'
)

high, critical = get_vulnerability_counts()

vuln_high.set(high)
vuln_critical.set(critical)

@app.route("/")
def home():
    return jsonify({"status": "running", "app": "SecureOps Pipeline"})

@app.route("/health")
def health():
    return jsonify({"healthy": True})

@app.route("/vuln-status")
def vuln_status():
    high, critical = get_vulnerability_counts()

    return jsonify({
        "high": high,
        "critical": critical,
        "status": "vulnerable" if (high > 0 or critical > 0) else "secure"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
