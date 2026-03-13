#!/usr/bin/env python3
import xml.etree.ElementTree as ET

def parse_nmap_xml(xml_file):
    findings = {"tool": "Nmap", "open_ports": [], "summary": {"total_open_ports": 0}}
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        open_count = 0

        for port in root.findall(".//port"):
            state = port.find(".//state")
            if state is not None and state.get("state") == "open":
                open_count += 1
                port_id = port.get("portid")
                service = port.find(".//service")
                service_name = service.get("name") if service is not None else "unknown"

                findings["open_ports"].append({
                    "port": port_id,
                    "service": service_name,
                    "state": "open"
                })

        findings["summary"]["total_open_ports"] = open_count
        return findings
    except Exception as e:
        return {"error": str(e), "summary": {"total_open_ports": 0}}
