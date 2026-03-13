#!/usr/bin/env python3
import json

def parse_zap_json(json_file):
    findings = {
        "tool": "OWASP ZAP",
        "vulnerabilities": [],
        "summary": {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0, "total": 0}
    }
    try:
        with open(json_file, 'r') as f:
            zap_data = json.load(f)

        alerts = []
        if "site" in zap_data:
            for site in zap_data["site"]:
                if "alerts" in site:
                    alerts.extend(site["alerts"])

        for alert in alerts:
            risk_code = alert.get("riskcode", "0")

            if risk_code == "3":
                findings["summary"]["high"] += 1
            elif risk_code == "2":
                findings["summary"]["medium"] += 1
            elif risk_code == "1":
                findings["summary"]["low"] += 1
            else:
                findings["summary"]["info"] += 1

        findings["summary"]["total"] = len(alerts)
        return findings
    except Exception as e:
        return {"error": str(e), "summary": {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0, "total": 0}}
