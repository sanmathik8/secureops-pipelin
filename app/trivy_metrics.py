import json

def get_vulnerability_counts(report_file="../trivy-report.json"):
    high = 0
    critical = 0

    try:
        with open(report_file, "r") as f:
            data = json.load(f)

        for result in data.get("Results", []):
            for vuln in result.get("Vulnerabilities", []):
                severity = vuln.get("Severity")

                if severity == "HIGH":
                    high += 1
                elif severity == "CRITICAL":
                    critical += 1

    except Exception as e:
        print(f"Error reading Trivy report: {e}")

    return high, critical
