import json

def get_vulnerabilities(report_file="trivy-report.json"):
    """reads trivy report and separates fixable and no-fix vulnerabilities"""
    with open(report_file) as f:
        data = json.load(f)
    
    fixable = {}
    no_fix = {}

    for result in data.get("Results", []):
        for vuln in result.get("Vulnerabilities", []):
            severity    = vuln.get("Severity")
            package     = vuln.get("PkgName")
            current_ver = vuln.get("InstalledVersion")
            fix_version = vuln.get("FixedVersion")
            cve_id      = vuln.get("VulnerabilityID")

            if severity in ["CRITICAL", "HIGH"] and package:
                if fix_version:
                    fixable[package] = {
                        "current": current_ver,
                        "fix_to": fix_version,
                        "cve": cve_id
                    }
                else:
                    no_fix[package] = {
                        "current": current_ver,
                        "cve": cve_id
                    }

    return fixable, no_fix


def generate_suggestion_report(fixable, no_fix, output_file="suggestions.txt"):
    """writes suggestion report to suggestions.txt without modifying any files"""
    with open(output_file, "w") as f:
        f.write("=" * 60 + "\n")
        f.write("  SECURITY SCAN REPORT — MANUAL ACTION REQUIRED\n")
        f.write("=" * 60 + "\n\n")

        if fixable:
            f.write("FIXABLE VULNERABILITIES:\n")
            f.write("-" * 40 + "\n")
            for pkg, info in fixable.items():
                f.write(f"  Package : {pkg}\n")
                f.write(f"  Current : {info['current']}\n")
                f.write(f"  Upgrade : {info['fix_to']}\n")
                f.write(f"  CVE     : {info['cve']}\n")
                f.write(f"  Action  : Please upgrade this package manually\n\n")

        if no_fix:
            f.write("NO FIX AVAILABLE YET:\n")
            f.write("-" * 40 + "\n")
            for pkg, info in no_fix.items():
                f.write(f"  Package : {pkg}\n")
                f.write(f"  Current : {info['current']}\n")
                f.write(f"  CVE     : {info['cve']}\n")
                f.write(f"  Action  : Monitor https://security-tracker.debian.org\n\n")

        f.write("=" * 60 + "\n")
        f.write("NOTE: No files were auto-modified.\n")
        f.write("Please review and apply fixes manually.\n")
        f.write("=" * 60 + "\n")


if __name__ == "__main__":
    print("Scanning trivy report...")
    fixable, no_fix = get_vulnerabilities()
    generate_suggestion_report(fixable, no_fix)
    print(f"Found {len(fixable)} fixable, {len(no_fix)} with no fix available.")
    print("Suggestion report saved to suggestions.txt")
    print("No files were auto-modified. Please review suggestions.txt")
