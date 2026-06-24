import json
import sys

with open("trivy-report.json", "r", encoding="utf-8") as f:
    data = json.load(f)

critical_vulns = []

for result in data.get("Results", []):
    for vuln in result.get("Vulnerabilities", []):

        if vuln.get("Severity") == "CRITICAL":
            critical_vulns.append({
                "PkgName": vuln.get("PkgName", "N/A"),
                "VulnerabilityID": vuln.get("VulnerabilityID", "N/A"),
                "InstalledVersion": vuln.get("InstalledVersion", "N/A"),
                "FixedVersion": vuln.get("FixedVersion", "Not Available"),
                "Severity": vuln.get("Severity")
            })

# Write file for Git issue stage
with open("critical.json", "w", encoding="utf-8") as f:
    json.dump(critical_vulns, f, indent=2)

# Also generate readable log file
with open("suggestions.txt", "w", encoding="utf-8") as report:
    report.write("SECURITY REPORT (CRITICAL ONLY)\n")
    report.write("=" * 50 + "\n\n")

    for v in critical_vulns:
        report.write(f"Package : {v['PkgName']}\n")
        report.write(f"CVE     : {v['VulnerabilityID']}\n")
        report.write(f"Current : {v['InstalledVersion']}\n")
        report.write(f"Fixed   : {v['FixedVersion']}\n")
        report.write("-" * 40 + "\n")

print(f"Critical vulnerabilities found: {len(critical_vulns)}")

# FAIL PIPELINE ONLY IF CRITICAL EXISTS
if len(critical_vulns) > 0:
    sys.exit(1)
else:
    sys.exit(0)
