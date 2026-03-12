#!/usr/bin/env python3
"""
Nmap Results Parser
Parses Nmap scan output and extracts key findings
"""

import json
import sys
import os
import xml.etree.ElementTree as ET
from datetime import datetime

def parse_nmap_xml(xml_file):
    """Parse Nmap XML output and extract open ports and services"""
    
    findings = {
        "scan_time": str(datetime.now()),
        "tool": "Nmap",
        "target": None,
        "open_ports": [],
        "summary": {}
    }
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Get target info
        host = root.find(".//host")
        if host is not None:
            address = host.find(".//address")
            if address is not None:
                findings["target"] = address.get("addr")
        
        # Extract open ports
        ports = root.findall(".//port")
        open_count = 0
        
        for port in ports:
            state = port.find(".//state")
            if state is not None and state.get("state") == "open":
                open_count += 1
                port_id = port.get("portid")
                protocol = port.get("protocol")
                service = port.find(".//service")
                service_name = service.get("name") if service is not None else "unknown"
                service_product = service.get("product") if service is not None else ""
                service_version = service.get("version") if service is not None else ""
                
                findings["open_ports"].append({
                    "port": port_id,
                    "protocol": protocol,
                    "service": service_name,
                    "product": service_product,
                    "version": service_version,
                    "state": "open"
                })
        
        findings["summary"]["total_open_ports"] = open_count
        
    except Exception as e:
        findings["error"] = str(e)
    
    return findings

def parse_nmap_text(text_file):
    """Fallback: Parse Nmap text output (simplified)"""
    
    findings = {
        "scan_time": str(datetime.now()),
        "tool": "Nmap",
        "open_ports": [],
        "summary": {}
    }
    
    try:
        with open(text_file, 'r') as f:
            content = f.read()
            
        # Simple regex-like extraction (simplified)
        import re
        port_pattern = r'(\d+)/tcp\s+open\s+(\S+)'
        matches = re.findall(port_pattern, content)
        
        for port, service in matches:
            findings["open_ports"].append({
                "port": port,
                "protocol": "tcp",
                "service": service,
                "state": "open"
            })
        
        findings["summary"]["total_open_ports"] = len(matches)
        
    except Exception as e:
        findings["error"] = str(e)
    
    return findings

if __name__ == "__main__":
    # If run directly, parse the first argument as file
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if file_path.endswith('.xml'):
            results = parse_nmap_xml(file_path)
        else:
            results = parse_nmap_text(file_path)
        
        print(json.dumps(results, indent=2))
    else:
        print("Usage: python parse_nmap.py <nmap_output_file>")
