#!/usr/bin/env python3
"""
ZAP Results Parser
Parses OWASP ZAP JSON output and extracts vulnerability findings
"""

import json
import sys
from datetime import datetime

def parse_zap_json(json_file):
    """Parse ZAP JSON report and extract vulnerabilities by risk level"""
    
    findings = {
        "scan_time": str(datetime.now()),
        "tool": "OWASP ZAP",
        "target": None,
        "vulnerabilities": [],
        "summary": {
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0,
            "total": 0
        }
    }
    
    try:
        with open(json_file, 'r') as f:
            zap_data = json.load(f)
        
        # Extract site information
        if "site" in zap_data and len(zap_data["site"]) > 0:
            findings["target"] = zap_data["site"][0].get("@name", "unknown")
        
        # Extract alerts
        alerts = []
        if "site" in zap_data:
            for site in zap_data["site"]:
                if "alerts" in site:
                    alerts.extend(site["alerts"])
        
        # Process each alert
        for alert in alerts:
            risk = alert.get("riskdesc", "").lower()
            vuln = {
                "name": alert.get("name", ""),
                "risk": alert.get("riskdesc", ""),
                "confidence": alert.get("confidence", ""),
                "description": alert.get("desc", ""),
                "solution": alert.get("solution", ""),
                "reference": alert.get("reference", ""),
                "instances": []
            }
            
            # Extract instances (URLs where found)
            if "instances" in alert:
                for instance in alert["instances"]:
                    vuln["instances"].append({
                        "uri": instance.get("uri", ""),
                        "method": instance.get("method", ""),
                        "param": instance.get("param", ""),
                        "evidence": instance.get("evidence", "")
                    })
            
            findings["vulnerabilities"].append(vuln)
            
            # Count by risk level
            if "high" in risk:
                findings["summary"]["high"] += 1
            elif "medium" in risk:
                findings["summary"]["medium"] += 1
            elif "low" in risk:
                findings["summary"]["low"] += 1
            else:
                findings["summary"]["info"] += 1
        
        findings["summary"]["total"] = len(alerts)
        
    except Exception as e:
        findings["error"] = str(e)
    
    return findings

def parse_zap_html_fallback(html_file):
    """Fallback: Create summary from HTML file existence"""
    # This is a simplified version - in practice, you'd parse HTML
    return {
        "scan_time": str(datetime.now()),
        "tool": "OWASP ZAP",
        "note": "HTML report available - manual review recommended",
        "file": html_file
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if file_path.endswith('.json'):
            results = parse_zap_json(file_path)
        else:
            results = parse_zap_html_fallback(file_path)
        
        print(json.dumps(results, indent=2))
    else:
        print("Usage: python parse_zap.py <zap_output.json>")
