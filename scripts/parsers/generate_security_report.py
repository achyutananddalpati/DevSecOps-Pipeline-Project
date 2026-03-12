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
            "failed_checks": [],
            "passed_checks": [],
            "recommendations": []
        }
    
    def load_nmap_results(self, file_path):
        """Load and parse Nmap results"""
        try:
            with open(file_path, 'r') as f:
                self.report["findings"]["nmap"] = json.load(f)
            self.report["passed_checks"].append("Nmap scan completed")
        except Exception as e:
            self.report["failed_checks"].append(f"Nmap parsing failed: {str(e)}")
    
    def load_zap_results(self, file_path):
        """Load and parse ZAP results"""
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
                
            self.report["passed_checks"].append("ZAP scan completed")
        except Exception as e:
            self.report["failed_checks"].append(f"ZAP parsing failed: {str(e)}")
    
    def load_exploit_results(self, file_path):
        """Load exploit verification results"""
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
        
        # Determine if pipeline should break (critical vulnerabilities cause failure)
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
    
    # Look for result files in common locations
    result_files = {
        'nmap': glob.glob("**/nmap*.json", recursive=True) + glob.glob("**/scan-results/*.json", recursive=True),
        'zap': glob.glob("**/zap*.json", recursive=True) + glob.glob("**/report_json.json", recursive=True),
        'exploits': glob.glob("**/sql_injection_results.json", recursive=True) + glob.glob("**/xss_results.json", recursive=True)
    }
    
    # Load each result type
    for file in result_files['nmap'][:1]:  # Take first found
        generator.load_nmap_results(file)
        break
    
    for file in result_files['zap'][:1]:
        generator.load_zap_results(file)
        break
    
    for file in result_files['exploits']:
        generator.load_exploit_results(file)
    
    # Generate and save report
    report = generator.generate()
    output_file = generator.save(f"security-report-{report['report_id']}.json")
    
    # Print summary to console
    print("\n" + "="*60)
    print("📊 SECURITY REPORT SUMMARY")
    print("="*60)
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
