import json

def get_vulnerable_packages(report_file="trivy-report.json"):
    vulnerable = {}
    with open(report_file) as f:
        data = json.load(f)
    for result in data.get("Results", []):
        for vuln in result.get("Vulnerabilities", []):
            severity    = vuln.get("Severity")
            package     = vuln.get("PkgName")
            fix_version = vuln.get("FixedVersion")
            if severity in ["CRITICAL", "HIGH"] and package and fix_version:
                vulnerable[package] = fix_version
    return vulnerable

def update_requirements(vulnerable_packages, req_file="app/requirements.txt"):
    with open(req_file) as f:
        lines = f.readlines()
    updated_lines = []
    for line in lines:
        package_name = line.split("==")[0].strip().lower()
        if package_name in vulnerable_packages:
            safe_version = vulnerable_packages[package_name]
            print(f"  Fixing: {package_name} → {safe_version}")
            updated_lines.append(f"{package_name}=={safe_version}\n")
        else:
            updated_lines.append(line)
    with open(req_file, "w") as f:
        f.writelines(updated_lines)

if __name__ == "__main__":
    print("Scanning trivy report for vulnerable packages...")
    vulnerable = get_vulnerable_packages()
    if vulnerable:
        print(f"Found {len(vulnerable)} packages to fix: {list(vulnerable.keys())}")
        update_requirements(vulnerable)
        print("Done! requirements.txt updated with safe versions.")
    else:
        print("No vulnerable packages found. Nothing to fix!")
