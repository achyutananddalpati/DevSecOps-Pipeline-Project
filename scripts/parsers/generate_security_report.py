#!/usr/bin/env python3
"""
Unified Security Report Generator
Combines results from all security tools into a single report
"""

import json
import sys
import os
import glob
from datetime import datetime

class SecurityReportGenerator:
    def __init__(self):
        self.report = {
            "report_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "generated_at": str(datetime.now()),
            "summary": {
                "total_vulnerabilities": 0,
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "info": 0
            },
            "findings": {
                "nmap": None,
                "zap": None,
                "exploits": None,
                "dependabot": None,
                "sonarqube": None
            },
            "files_found": [],  # NEW: Track what files were found
            "failed_checks": [],
            "passed_checks": [],
            "recommendations": []
        }

    def load_nmap_results(self, file_path):
        """Load and parse Nmap results"""
        self.report["files_found"].append(f"nmap: {file_path}")
        try:
            with open(file_path, 'r') as f:
                self.report["findings"]["nmap"] = json.load(f)
            self.report["passed_checks"].append("Nmap scan completed")
        except Exception as e:
            self.report["failed_checks"].append(f"Nmap parsing failed: {str(e)}")

    def load_zap_results(self, file_path):
        """Load and parse ZAP results"""
        self.report["files_found"].append(f"zap: {file_path}")
        try:
            with open(file_path, 'r') as f:
                zap_data = json.load(f)
                self.report["findings"]["zap"] = zap_data

                # Add to summary
                if "summary" in zap_data:
                    self.report["summary"]["high"] += zap_data["summary"].get("high", 0)
                    self.report["summary"]["medium"] += zap_data["summary"].get("medium", 0)
                    self.report["summary"]["low"] += zap_data["summary"].get("low", 0)
                    self.report["summary"]["info"] += zap_data["summary"].get("info", 0)
                else:
                    # Try to count from vulnerabilities
                    if "vulnerabilities" in zap_data:
                        for vuln in zap_data["vulnerabilities"]:
                            risk = vuln.get("risk", "").lower()
                            if "high" in risk:
                                self.report["summary"]["high"] += 1
                            elif "medium" in risk:
                                self.report["summary"]["medium"] += 1
                            elif "low" in risk:
                                self.report["summary"]["low"] += 1
                            else:
                                self.report["summary"]["info"] += 1

            self.report["passed_checks"].append("ZAP scan completed")
        except Exception as e:
            self.report["failed_checks"].append(f"ZAP parsing failed: {str(e)}")

    def load_exploit_results(self, file_path):
        """Load exploit verification results"""
        self.report["files_found"].append(f"exploits: {file_path}")
        try:
            with open(file_path, 'r') as f:
                exploit_data = json.load(f)
                self.report["findings"]["exploits"] = exploit_data

                # Count verified exploits
                if "vulnerabilities" in exploit_data:
                    verified = len(exploit_data["vulnerabilities"])
                    if verified > 0:
                        self.report["summary"]["critical"] += verified
                        self.report["failed_checks"].append(f"{verified} exploits VERIFIED")
                elif isinstance(exploit_data, list):
                    verified = len(exploit_data)
                    if verified > 0:
                        self.report["summary"]["critical"] += verified
                        self.report["failed_checks"].append(f"{verified} exploits VERIFIED")

            self.report["passed_checks"].append("Exploit verification completed")
        except Exception as e:
            self.report["failed_checks"].append(f"Exploit parsing failed: {str(e)}")

    def generate(self):
        """Generate final report with recommendations"""

        # Calculate total
        self.report["summary"]["total_vulnerabilities"] = (
            self.report["summary"]["critical"] +
            self.report["summary"]["high"] +
            self.report["summary"]["medium"] +
            self.report["summary"]["low"] +
            self.report["summary"]["info"]
        )

        # Generate recommendations based on findings
        if self.report["summary"]["critical"] > 0:
            self.report["recommendations"].append("🔴 CRITICAL: Fix critical vulnerabilities immediately - pipeline will fail")

        if self.report["summary"]["high"] > 5:
            self.report["recommendations"].append("🟡 HIGH: Prioritize fixing high-risk vulnerabilities")

        if self.report["findings"]["nmap"] and len(self.report["findings"]["nmap"].get("open_ports", [])) > 10:
            self.report["recommendations"].append("🔓 Many open ports detected - review firewall rules")

        if len(self.report["files_found"]) == 0:
            self.report["recommendations"].append("⚠️ No scan artifacts were found. Run scan workflows first!")

        # Determine if pipeline should break
        self.report["pipeline_status"] = "FAILED" if self.report["summary"]["critical"] > 0 else "PASSED"

        return self.report

    def save(self, output_file="security-report.json"):
        """Save report to file"""
        with open(output_file, 'w') as f:
            json.dump(self.report, f, indent=2)
        print(f"✅ Report saved to {output_file}")
        return output_file

def main():
    generator = SecurityReportGenerator()

    # First, check current directory and parent
    print(f"Current working directory: {os.getcwd()}")
    print("Searching for JSON files...")

    # Look for result files in common locations
    search_paths = [
        "./scan-results",
        "../../scan-results",
        "../",
        "."
    ]

    for path in search_paths:
        if os.path.exists(path):
            print(f"Searching in: {path}")
            nmap_files = glob.glob(f"{path}/**/nmap*.json", recursive=True) + glob.glob(f"{path}/**/*nmap*.json", recursive=True)
            zap_files = glob.glob(f"{path}/**/zap*.json", recursive=True) + glob.glob(f"{path}/**/report_json.json", recursive=True)
            exploit_files = glob.glob(f"{path}/**/sql_injection_results.json", recursive=True) + glob.glob(f"{path}/**/xss_results.json", recursive=True)

            if nmap_files:
                print(f"Found Nmap files: {nmap_files}")
                for file in nmap_files:
                    generator.load_nmap_results(file)
                    break  # Take first only

            if zap_files:
                print(f"Found ZAP files: {zap_files}")
                for file in zap_files:
                    generator.load_zap_results(file)
                    break  # Take first only

            if exploit_files:
                print(f"Found exploit files: {exploit_files}")
                for file in exploit_files:
                    generator.load_exploit_results(file)

    # Generate and save report
    report = generator.generate()
    output_file = generator.save(f"security-report-{report['report_id']}.json")

    # Print summary to console
    print("\n" + "="*60)
    print("📊 SECURITY REPORT SUMMARY")
    print("="*60)
    print(f"Files found: {len(report['files_found'])}")
    for f in report['files_found']:
        print(f"  - {f}")
    print("-"*60)
    print(f"Critical: {report['summary']['critical']}")
    print(f"High:     {report['summary']['high']}")
    print(f"Medium:   {report['summary']['medium']}")
    print(f"Low:      {report['summary']['low']}")
    print(f"Info:     {report['summary']['info']}")
    print("="*60)
    print(f"Pipeline Status: {report['pipeline_status']}")
    print("="*60)

    # Print recommendations
    if report['recommendations']:
        print("\n🔍 RECOMMENDATIONS:")
        for rec in report['recommendations']:
            print(f"  • {rec}")

if __name__ == "__main__":
    main()
