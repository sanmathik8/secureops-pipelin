import json
import os

def get_vulnerability_counts():

    high = 0
    critical = 0

    report_file = "/app/trivy-report.json"

    if not os.path.exists(report_file):
        return 0, 0

    with open(report_file) as file:
        data = json.load(file)

    for result in data.get("Results", []):

        for vuln in result.get("Vulnerabilities", []):

            if vuln.get("Severity") == "HIGH":
                high += 1

            elif vuln.get("Severity") == "CRITICAL":
                critical += 1

    return high, critical
