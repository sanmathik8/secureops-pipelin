import json, sys

with open("trivy-report.json") as f:
    data = json.load(f)

critical_vulns = []

for result in data.get("Results", []):
    for vuln in result.get("Vulnerabilities", []):
        if vuln.get("Severity") == "CRITICAL":
            critical_vulns.append({
                "package" : vuln.get("PkgName"),
                "current" : vuln.get("InstalledVersion"),
                "fix"     : vuln.get("FixedVersion") or "NO FIX AVAILABLE",
                "cve"     : vuln.get("VulnerabilityID")
            })

if critical_vulns:
    print("\n CRITICAL Vulnerabilities Found — Deployment Blocked!\n")
    print("-" * 55)
    for v in critical_vulns:
        print(f"  Package : {v['package']}")
        print(f"  Version : {v['current']}")
        print(f"  Fix     : {v['fix']}")
        print(f"  CVE     : {v['cve']}")
        print()
    print("-" * 55)
    print(f"  Total Critical : {len(critical_vulns)}")
    print("  Action  : Review suggestions.txt for remediation steps")
    print("-" * 55)
    sys.exit(1)
else:
    print("No CRITICAL vulnerabilities found. Deployment allowed!")
