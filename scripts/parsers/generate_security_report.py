#!/usr/bin/env python3
import json
import os
import glob
from datetime import datetime
from parse_nmap import parse_nmap_xml
from parse_zap import parse_zap_json

class SecurityReportGenerator:
    def __init__(self):
        self.report = {
            "report_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "summary": {"total_vulnerabilities": 0, "critical": 0, "high": 0, "medium": 0, "low": 0},
            "findings": {"nmap": None, "zap": None},
            "pipeline_status": "PASSED"
        }

    def generate(self):
        # 1. Search for ZAP JSON files anywhere in the workspace
        zap_files = glob.glob("**/*zap*.json", recursive=True) + glob.glob("**/report_json.json", recursive=True)
        if zap_files:
            print(f"[+] Found ZAP artifact: {zap_files[0]}")
            self.report["findings"]["zap"] = parse_zap_json(zap_files[0])
            zap_sum = self.report["findings"]["zap"].get("summary", {})
            self.report["summary"]["high"] += zap_sum.get("high", 0)
            self.report["summary"]["medium"] += zap_sum.get("medium", 0)

        # 2. Search for Nmap XML files anywhere in the workspace
        nmap_files = glob.glob("**/*nmap*.xml", recursive=True)
        if nmap_files:
            print(f"[+] Found Nmap artifact: {nmap_files[0]}")
            self.report["findings"]["nmap"] = parse_nmap_xml(nmap_files[0])

        # 3. Calculate Totals and Pipeline Status
        self.report["summary"]["total_vulnerabilities"] = sum([
            self.report["summary"]["critical"],
            self.report["summary"]["high"],
            self.report["summary"]["medium"]
        ])

        # FAIL THE PIPELINE IF HIGH VULNERABILITIES EXIST
        if self.report["summary"]["high"] > 0 or self.report["summary"]["critical"] > 0:
            self.report["pipeline_status"] = "FAILED"

        return self.report

    def save(self):
        output_file = f"security-report-{self.report['report_id']}.json"
        with open(output_file, 'w') as f:
            json.dump(self.report, f, indent=2)
        return output_file

if __name__ == "__main__":
    print("🔍 Initializing Unified Security Report Generator...")
    generator = SecurityReportGenerator()
    report = generator.generate()
    generator.save()

    print("\n" + "="*40)
    print("📊 FINAL SECURITY REPORT SUMMARY")
    print("="*40)
    print(f"High Vulnerabilities:   {report['summary']['high']}")
    print(f"Medium Vulnerabilities: {report['summary']['medium']}")
    print("="*40)
    print(f"PIPELINE STATUS:        {report['pipeline_status']}")
    print("="*40 + "\n")
