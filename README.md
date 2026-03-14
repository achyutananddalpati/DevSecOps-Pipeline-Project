# Implementation of an Automated DevSecOps Pipeline using a Hybrid Cloud Architecture for Enhanced Security

## Project Overview
This project modernizes traditional penetration testing by transitioning manual testing tasks into an automated Continuous Integration/Continuous Deployment (CI/CD) pipeline. Using a hybrid architecture, development and scripting are handled on a local Linux machine, automation and security scanning are offloaded to GitHub Actions (cloud CI/CD), and the target application is hosted on a dedicated AWS Virtual Private Server (VPS).

---

## Chapter 1: Perform Hybrid Environment Setup (Replaces Traditional Footprinting)

### Completed Tasks:

#### a. Local Development Environment ✅
- **Operating System:** Arch Linux
- **Tools Installed:** 
  - Visual Studio Code (Code editor)
  - Git (Version control)
  - SSH client for server access

#### b. Cloud Target Provisioning ✅
- **Cloud Provider:** AWS (Amazon Web Services)
- **Instance Type:** t2.micro (Free tier eligible)
- **Operating System:** Ubuntu Server 22.04 LTS
- **Region:** ap-south-1 (Mumbai)
- **Public IP:** ---------
- **Public DNS:** ---------
- **Key Pair:** devsecops-key.pem (stored locally, protected by .gitignore)

#### c. Vulnerable Application Deployment ✅
- **Application:** OWASP Juice Shop (Intentionally vulnerable web app)
- **Deployment Method:** Docker container
- **Container Name:** juice-shop
- **Port Mapping:** 80:3000 (Host:Container)
- **Access URL:** http://***********
- **Auto-start:** Configured with restart policy

#### d. Pipeline Initialization ✅
- **Version Control:** Git initialized locally
- **Remote Repository:** GitHub (DevSecOps-Pipeline-Project)
- **CI/CD Platform:** GitHub Actions
- **Workflow Created:** 01-info-gathering.yml
- **GitHub Secrets Configured:**
  - `AWS_SERVER_IP`: ----------
  - `AWS_SERVER_DOMAIN`: ---------

---

## Chapter 2: Perform Automated Information Gathering

### Planned Tasks:

#### a. Automated Port Scanning
- Implement Nmap scanning in GitHub Actions
- Scan target AWS server for open ports
- Identify unintended entry points
- Automate on every code push

#### b. Service Identification
- Verify SSH service security
- Check FTP service status
- Identify running services on open ports
- Generate service inventory

#### c. Continuous Secret Scanning
- Integrate TruffleHog in pipeline
- Scan source code for exposed API keys
- Hunt for passwords in codebase
- Automated alerts on secret detection

---

## Chapter 3: Perform Automated Vulnerability Scanning

### Planned Tasks:

#### a. Dynamic Application Security Testing (DAST)
- Integrate OWASP ZAP in GitHub Actions
- Attack running application on AWS server
- Identify runtime vulnerabilities
- Replace legacy tools (WMAP, NESSUS)

#### b. Static Application Security Testing (SAST)
- Configure SonarQube in pipeline
- Scan application source code
- Identify underlying code flaws
- Pre-deployment security validation

---

## Chapter 4: Perform Automated Exploitation, Verification & SCA

### Planned Tasks:

#### a. Exploit Scripting (Stateless Verification)
- Write custom Python scripts locally
- Push scripts to GitHub for execution
- Send malicious payloads (SQL Injection, XSS)
- Analyze server responses
- Bypass firewall limitations

#### b. Software Composition Analysis (SCA)
- Configure GitHub Dependabot
- Scan for outdated libraries
- Identify supply chain vulnerabilities
- Track third-party dependencies

---

## Chapter 5: Perform Automated Reporting & Pipeline Breaking

### Planned Tasks:

#### a. Ingesting Scan Results & Pipeline Failure
- Ingest JSON/XML output from Nmap and ZAP scans
- Parse scan results into a unified security report with risk categorization
- Automatically fail the pipeline (exit code 1) when high/critical vulnerabilities found
- Halt deployment process to enforce security quality gates
- Generate downloadable artifact with complete findings

#### c. Real-Time Alerting
- Set up webhooks for notifications
- Integrate Slack channel alerts
- Immediate failure reporting

---

## Chapter 6: Perform Mitigation and Remediation

### Planned Tasks:

#### a. Manual Code Remediation
- Patch vulnerable code locally
- Fix issues identified by DAST/SAST
- Implement security fixes

#### b. Automated Dependency Updates
- Allow Dependabot to create Pull Requests
- Update vulnerable libraries automatically
- Merge secure versions

#### c. Pipeline Validation
- Push fixed code to trigger pipeline
- Re-run all security scans
- Verify vulnerability fixes

#### d. Secure Deployment
- Pass all security checks
- Deploy hardened application to AWS
- Final validation complete

---

## Technology Stack

| Component | Technology Used |
|-----------|-----------------|
| **Local OS** | Arch Linux |
| **Code Editor** | Visual Studio Code |
| **Version Control** | Git |
| **Remote Repository** | GitHub |
| **CI/CD Platform** | GitHub Actions |
| **Cloud Provider** | AWS EC2 |
| **Target OS** | Ubuntu Server 22.04 LTS |
| **Vulnerable App** | OWASP Juice Shop |
| **Container Platform** | Docker |
| **Port Scanner** | Nmap |
| **Secret Scanner** | TruffleHog |
| **DAST Scanner** | OWASP ZAP |
| **SAST Scanner** | SonarQube |
| **SCA Tool** | GitHub Dependabot |
| **Alerting** | Slack/Email Webhooks |

---
