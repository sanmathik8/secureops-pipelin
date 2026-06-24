import json

with open("trivy-report.json") as f:
    data = json.load(f)

report = open("suggestions.txt", "w")

report.write("SECURITY SCAN REPORT\n")
report.write("=" * 50 + "\n\n")

for result in data["Results"]:

    if "Vulnerabilities" not in result:
        continue

    for vuln in result["Vulnerabilities"]:

        if vuln["Severity"] not in ["HIGH", "CRITICAL"]:
            continue

        report.write(f"Package : {vuln['PkgName']}\n")
        report.write(f"CVE     : {vuln['VulnerabilityID']}\n")
        report.write(f"Current : {vuln['InstalledVersion']}\n")

        if vuln["FixedVersion"]:
            report.write(f"Upgrade : {vuln['FixedVersion']}\n")
            report.write("Action  : Upgrade this package.\n\n")
        else:
            report.write("Upgrade : No fix available.\n")
            report.write("Action  : Monitor Debian Security Tracker.\n\n")

report.close()

print("Suggestion report generated successfully.")
