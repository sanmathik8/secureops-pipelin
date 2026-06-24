import json

def get_vulnerability_counts():

    high = 0
    critical = 0

    with open("../trivy-report.json") as file:
        data = json.load(file)

    for result in data["Results"]:

        for vuln in result["Vulnerabilities"]:

            if vuln["Severity"] == "HIGH":
                high = high + 1

            elif vuln["Severity"] == "CRITICAL":
                critical = critical + 1

    return high, critical
