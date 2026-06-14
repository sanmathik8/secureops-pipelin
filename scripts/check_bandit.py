import json, sys

try:
    with open("bandit-report.json") as f:
        data = json.load(f)
except Exception as e:
    print(f"Could not read bandit-report.json: {e}")
    sys.exit(1)

results = data.get("results", [])
highs = [r for r in results if r.get("issue_severity") == "HIGH"]

print(f"\n Bandit SAST Results")
print(f"  Total issues : {len(results)}")
print(f"  HIGH severity: {len(highs)}")

for h in highs:
    print(f"\n  [{h['issue_severity']}] {h['issue_text']}")
    print(f"   File   : {h['filename']}:{h['line_number']}")
    print(f"   Test ID: {h['test_id']}")

if highs:
    print("\n HIGH severity issues found. Failing pipeline.")
    sys.exit(1)
else:
    print("\n No HIGH severity issues. Bandit scan passed.")
