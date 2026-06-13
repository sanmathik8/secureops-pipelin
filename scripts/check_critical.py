import json, sys

with open('trivy-report.json') as f:
    data = json.load(f)

critical = sum(
    1 for r in data.get('Results', [])
    for v in r.get('Vulnerabilities', [])
    if v.get('Severity') == 'CRITICAL'
)

print('CRITICAL vulnerabilities found: ' + str(critical))

if critical > 0:
    sys.exit(1)
