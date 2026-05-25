# 🔐 Implementation of Automated DevSecOps Pipeline Using Hybrid Cloud Architecture for Enhanced Security

<p align="center">
  <img src="https://img.shields.io/badge/DevSecOps-Automated-blue?style=for-the-badge&logo=githubactions&logoColor=white"/>
  <img src="https://img.shields.io/badge/Cloud-AWS%20EC2-orange?style=for-the-badge&logo=amazonaws&logoColor=white"/>
  <img src="https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white"/>
  <img src="https://img.shields.io/badge/DAST-OWASP%20ZAP-black?style=for-the-badge&logo=owasp&logoColor=white"/>
  <img src="https://img.shields.io/badge/SAST-SonarQube-4E9BCD?style=for-the-badge&logo=sonarqube&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-Exploit%20Automation-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
</p>

<p align="center">
  <strong>A fully automated, end-to-end DevSecOps pipeline that embeds security into every stage of the CI/CD lifecycle using a hybrid cloud architecture.</strong>
</p>

---

## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Architecture Overview](#-architecture-overview)
- [Pipeline Workflow](#-pipeline-workflow)
- [Technology Stack](#-technology-stack)
- [Security Tools Integrated](#-security-tools-integrated)
- [Key Features](#-key-features)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [GitHub Actions Workflows](#-github-actions-workflows)
- [Security Findings Summary](#-security-findings-summary)
- [Automated Reporting & Alerts](#-automated-reporting--alerts)
- [Results & Validation](#-results--validation)
- [Limitations](#-limitations)
- [Future Recommendations](#-future-recommendations)
- [Workflow Execution Logs](#-workflow-execution-logs)
- [Security Assessment Reports](#-security-assessment-reports)
- [Author](#-author)

---

## 📖 About the Project

Modern software development increasingly relies on CI/CD pipelines to ship applications rapidly. However, this speed often introduces security risks when testing is overlooked during development. Traditional penetration testing is slow, manual, and incompatible with today's fast release cycles.

This project solves this problem by building a **fully automated DevSecOps pipeline** that strengthens web application security using a **hybrid cloud environment** for testing and deployment. Security is embedded directly into the Software Development Life Cycle (SDLC) through:

- ✅ **Automated vulnerability assessments**
- ✅ **Static and Dynamic Application Security Testing (SAST & DAST)**
- ✅ **Secret scanning and dependency monitoring**
- ✅ **Automated exploit verification using Python scripts**
- ✅ **Real-time alerting via Slack webhooks**
- ✅ **Secure cloud deployment with HTTPS and Nginx reverse proxy**

> **Target Application:** [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) — a deliberately insecure web application — hosted on AWS EC2 as the security testing testbed.

---

## 🏗️ Architecture Overview

The project uses a **hybrid cloud model**:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HYBRID CLOUD ARCHITECTURE                    │
│                                                                     │
│  ┌──────────────────┐          ┌────────────────────────────────┐  │
│  │   LOCAL MACHINE  │  push    │         GITHUB (Cloud)         │  │
│  │                  │ ──────►  │                                │  │
│  │  - Arch Linux    │          │  - Source Code Repository      │  │
│  │  - VS Code       │          │  - GitHub Actions CI/CD        │  │
│  │  - Git           │          │  - Dependabot (SCA)            │  │
│  │  - Exploit       │          │  - GitHub Security Issues      │  │
│  │    Scripts       │          │  - Artifacts Storage           │  │
│  └──────────────────┘          └───────────┬────────────────────┘  │
│                                            │ triggers               │
│                                            ▼                        │
│                              ┌─────────────────────────┐           │
│                              │      AWS EC2 (Cloud)     │           │
│                              │                          │           │
│                              │  - Ubuntu Server 22.04   │           │
│                              │  - OWASP Juice Shop      │           │
│                              │    (Docker Container)    │           │
│                              │  - Nginx + HTTPS/SSL     │           │
│                              │  - Nmap, ZAP, TruffleHog │           │
│                              │  - SonarQube Analysis    │           │
│                              │  - Slack Notifications   │           │
│                              └─────────────────────────┘           │
└─────────────────────────────────────────────────────────────────────┘
```

- **Local Environment:** Code development, workflow authoring, and exploit script creation on Arch Linux.
- **GitHub:** Source code management, CI/CD automation, dependency monitoring, and artifact storage.
- **AWS EC2 (Ubuntu Server):** Hosts the vulnerable application, runs automated security scans, and validates deployment.

---

## 🔄 Pipeline Workflow

Every push to the GitHub repository triggers the following automated security stages in sequence:

```
Code Push to GitHub
        │
        ▼
┌───────────────────┐
│ 1. Info Gathering │  ◄── Nmap: Open ports, services, infrastructure exposure
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 2. Secret Scan    │  ◄── TruffleHog: API keys, tokens, SSH credentials
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 3. SAST (Static)  │  ◄── SonarQube: Insecure code, logic flaws, code smells
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 4. DAST (Runtime) │  ◄── OWASP ZAP: SQLi, XSS, broken auth, insecure headers
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 5. Exploit Verify │  ◄── Python Scripts: Payload execution & confirmation
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 6. Dependency SCA │  ◄── Dependabot: Vulnerable 3rd-party packages
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 7. Report + Alert │  ◄── JSON Reports + Slack Webhooks (real-time alerts)
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 8. Deploy + HTTPS │  ◄── Nginx + SSL + AWS Security Group Hardening
└───────────────────┘
```

---

## 🛠️ Technology Stack

| Category | Tool / Technology | Purpose |
|---|---|---|
| **Version Control** | Git | Source code management |
| **Remote Repository** | GitHub | Code hosting and collaboration |
| **Local OS** | Arch Linux | Local development environment |
| **Code Editor** | Visual Studio Code | Workflow and exploit development |
| **CI/CD Platform** | GitHub Actions | Workflow automation and orchestration |
| **Cloud Platform** | AWS EC2 | Cloud-hosted deployment infrastructure |
| **Target OS** | Ubuntu Server 22.04 LTS | Cloud server environment |
| **Vulnerable App** | OWASP Juice Shop | Security testing target (Dockerized) |
| **Container Platform** | Docker | Application containerization |
| **Scripting Language** | Python | Exploit verification automation |
| **Reverse Proxy** | Nginx | HTTPS and secure traffic management |
| **Alerting** | Slack Webhooks | Real-time security notifications |

---

## 🔒 Security Tools Integrated

| Tool | Category | Function |
|---|---|---|
| **Nmap** | Network Scanner | Port scanning, service identification, infrastructure exposure |
| **TruffleHog** | Secret Scanner | Detection of exposed API keys, tokens, SSH credentials |
| **SonarQube** | SAST | Static source code analysis and vulnerability detection |
| **OWASP ZAP** | DAST | Runtime vulnerability scanning (SQLi, XSS, auth flaws) |
| **Dependabot** | SCA | Dependency vulnerability monitoring and alerts |
| **Python Scripts** | Exploit Verification | Automated payload execution and vulnerability validation |
| **Slack Webhooks** | Alerting | Real-time pipeline and vulnerability notifications |
| **Nginx + SSL** | Infrastructure Security | HTTPS enforcement and reverse proxy hardening |

---

## ✨ Key Features

- 🔁 **Fully Automated Pipeline** — Security testing triggers automatically on every code push, with zero manual intervention.
- 🧪 **Multi-Stage Security Testing** — Combines SAST, DAST, network scanning, secret detection, SCA, and exploit verification in a unified workflow.
- ☁️ **Hybrid Cloud Architecture** — Local development integrated with cloud-based CI/CD and deployment for scalability and efficiency.
- 🐍 **Automated Exploit Verification** — Custom Python scripts validate whether identified vulnerabilities (SQLi, XSS) are actually exploitable.
- 📊 **Centralized JSON Reporting** — Vulnerability findings are structured in JSON format for automated parsing and analysis.
- 🔔 **Real-Time Slack Alerts** — Instant notifications on vulnerability discovery, workflow status, and pipeline failures.
- 🚫 **Pipeline Gate on Critical Findings** — Deployment is automatically halted when high/critical vulnerabilities are detected.
- 🔐 **Secure Deployment** — HTTPS via Nginx reverse proxy + SSL certificate + AWS Security Group hardening.
- 📋 **Automated GitHub Issue Tracking** — Security findings are automatically logged as GitHub Issues for centralized tracking.

---

## 📁 Project Structure

```
DevSecOps-Pipeline-Project/
│
├── .github/
│   └── workflows/                  # GitHub Actions CI/CD workflow files
│       ├── information-gathering.yml
│       ├── nmap-scan.yml
│       ├── service-identification.yml
│       ├── secret-scanning.yml
│       ├── owasp-zap-dast.yml
│       ├── sonarqube-sast.yml
│       ├── exploit-verification.yml
│       └── security-reporting-alert.yml
│
├── exploits/                       # Custom Python exploit verification scripts
│   ├── sqli_verify.py
│   └── xss_verify.py
│
├── scripts/
│   └── parsers/                    # JSON vulnerability report parsers
│
├── sonar-project.properties        # SonarQube project configuration
├── requirements.txt                # Python dependencies
├── connect-to-server.sh            # AWS EC2 SSH connection helper
├── aws-server-info.txt             # EC2 instance details (non-sensitive)
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- AWS account with EC2 access
- GitHub account with Actions enabled
- Slack workspace (for webhook notifications)
- SonarQube / SonarCloud account
- Docker installed on the EC2 instance

### 1. Clone the Repository

```bash
git clone https://github.com/achyutananddalpati/DevSecOps-Pipeline-Project.git
cd DevSecOps-Pipeline-Project
```

### 2. Provision AWS EC2 Instance

Launch an Ubuntu Server 22.04 LTS EC2 instance and note the public IP address.

```bash
# Connect to your EC2 instance
chmod +x connect-to-server.sh
./connect-to-server.sh
```

### 3. Deploy OWASP Juice Shop on EC2

```bash
# On the EC2 instance
docker pull bkimminich/juice-shop
docker run -d -p 3000:3000 bkimminich/juice-shop
```

### 4. Configure GitHub Secrets

Navigate to **Settings → Secrets and Variables → Actions** in your repository and add:

| Secret Name | Description |
|---|---|
| `EC2_HOST` | Public IP of your AWS EC2 instance |
| `EC2_SSH_KEY` | SSH private key for EC2 access |
| `SONAR_TOKEN` | SonarQube authentication token |
| `SONAR_HOST_URL` | SonarQube server URL |
| `SLACK_WEBHOOK_URL` | Slack incoming webhook URL |

### 5. Configure Nginx Reverse Proxy with HTTPS

```nginx
server {
    listen 443 ssl;
    server_name your-domain-or-ip;

    ssl_certificate     /etc/ssl/certs/your-cert.pem;
    ssl_certificate_key /etc/ssl/private/your-key.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 6. Trigger the Pipeline

Push any code change to the `main` branch to trigger the full automated security pipeline:

```bash
git add .
git commit -m "trigger: run DevSecOps pipeline"
git push origin main
```

---

## ⚙️ GitHub Actions Workflows

| # | Workflow | Trigger | Purpose |
|---|---|---|---|
| 1 | `information-gathering.yml` | Push to main | Initial reconnaissance and environment setup |
| 2 | `nmap-scan.yml` | Push to main | Network port and service scanning |
| 3 | `service-identification.yml` | Push to main | Identify active services and exposure |
| 4 | `secret-scanning.yml` | Push to main | TruffleHog credential detection |
| 5 | `owasp-zap-dast.yml` | Push to main | Runtime vulnerability scanning with ZAP |
| 6 | `sonarqube-sast.yml` | Push to main | Static source code analysis |
| 7 | `exploit-verification.yml` | Push to main | Python-based exploit payload validation |
| 8 | `security-reporting-alert.yml` | Push to main | JSON report generation + Slack alerts |

**Sample GitHub Actions Snippet (OWASP ZAP DAST):**

```yaml
- name: Run OWASP ZAP Scan
  run: |
    docker run -t owasp/zap2docker-stable zap-baseline.py \
      -t http://${{ secrets.EC2_HOST }}:3000 \
      -r zap_report.html
```

---

## 🔍 Security Findings Summary

### Network Scan (Nmap)

| Port | Service | Status |
|---|---|---|
| 22 | SSH | Open (admin access) |
| 80 | HTTP | Open (web traffic) |
| 443 | HTTPS | Open (SSL secured) |

### Static Analysis (SonarQube SAST)

| Vulnerability Type | Severity |
|---|---|
| Security Hotspot | Medium |
| Vulnerable Logic | High |
| Code Smell | Low |
| Maintainability Issue | Medium |

### Dynamic Analysis (OWASP ZAP DAST)

| Vulnerability | Severity |
|---|---|
| SQL Injection | High |
| Cross-Site Scripting (XSS) | Medium |
| Missing Security Headers | Medium |
| Insecure Session Handling | Medium |
| Information Disclosure | Low |

### Secret & Dependency Scanning

| Tool | Finding |
|---|---|
| TruffleHog | Exposed secret detected in repository |
| Dependabot | Vulnerable dependency identified |
| GitHub Security Alerts | Automated issue created and tracked |

---

## 📢 Automated Reporting & Alerts

**Python Exploit Verification Snippet:**

```python
import requests

target_url = "http://<EC2_PUBLIC_IP>:3000"
response = requests.get(target_url)
print("Status Code:", response.status_code)
print("Response Length:", len(response.text))
```

**Slack Notification Types:**

| Notification | Status |
|---|---|
| Workflow started/completed | ✅ Delivered |
| Vulnerability discovered | ✅ Generated |
| Pipeline failure alert | ✅ Delivered |
| Critical finding — deployment halted | ✅ Triggered |

---

## ✅ Results & Validation

| Validation Area | Result |
|---|---|
| AWS EC2 Deployment | ✅ Successful |
| OWASP Juice Shop Hosting | ✅ Active & Accessible |
| GitHub Actions CI/CD | ✅ All workflows executed |
| Network Scanning (Nmap) | ✅ Open ports identified |
| SAST (SonarQube) | ✅ Hotspots and code issues detected |
| DAST (OWASP ZAP) | ✅ SQLi, XSS, headers detected |
| Exploit Verification | ✅ Runtime vulnerabilities confirmed |
| Secret Scanning | ✅ Credential exposure detected |
| Dependency Monitoring | ✅ Vulnerable packages flagged |
| Slack Alert Notifications | ✅ Real-time delivery verified |
| HTTPS / Nginx / SSL | ✅ Secure communication validated |
| End-to-End Pipeline | ✅ Fully operational |

---

## ⚠️ Limitations

- Tested against a single application (OWASP Juice Shop); multi-app validation not in scope.
- Deployed exclusively on AWS EC2; multi-cloud (Azure, GCP) support not implemented.
- No automated vulnerability remediation — findings are reported but patching is manual.
- No AI/ML-based behavioral analysis or anomaly detection.
- Enterprise-grade scalability testing was not performed.
- Container orchestration (Kubernetes) not integrated in this iteration.
- Full SOC/SIEM integration was not implemented.

---

## 🔮 Future Recommendations

- 🤖 **AI-Driven Threat Detection** — Integrate ML-based anomaly detection for sophisticated threat identification.
- ☸️ **Kubernetes Integration** — Add container orchestration security for large-scale cloud-native deployments.
- ☁️ **Multi-Cloud Support** — Extend to Azure and GCP for broader coverage and resilience.
- 🔧 **Automated Remediation** — Implement self-healing mechanisms to auto-patch known vulnerabilities.
- 📊 **SIEM Integration** — Connect to a centralized Security Information and Event Management platform.
- 🔑 **Secrets Management** — Integrate HashiCorp Vault or AWS Secrets Manager for secure credential storage.
- 📱 **Multi-Channel Alerting** — Add WhatsApp/Gmail notifications in addition to Slack.
- ✅ **Compliance Automation** — Embed regulatory compliance checks (PCI-DSS, HIPAA) into the pipeline.

---

## 📋 Workflow Execution Logs

| Workflow | GitHub Actions Log |
|---|---|
| Information Gathering | [View Log](https://github.com/achyutananddalpati/DevSecOps-Pipeline-Project/actions/runs/23406901215) |
| Nmap Scan | [View Log](https://github.com/achyutananddalpati/DevSecOps-Pipeline-Project/actions/runs/23406930949) |
| Service Identification | [View Log](https://github.com/achyutananddalpati/DevSecOps-Pipeline-Project/actions/runs/23406971607) |
| Secret Scanning | [View Log](https://github.com/achyutananddalpati/DevSecOps-Pipeline-Project/actions/runs/23407006481) |
| OWASP ZAP DAST | [View Log](https://github.com/achyutananddalpati/DevSecOps-Pipeline-Project/actions/runs/23407035447) |
| SonarQube SAST | [View Log](https://github.com/achyutananddalpati/DevSecOps-Pipeline-Project/actions/runs/23408578464) |
| Exploit Verification | [View Log](https://github.com/achyutananddalpati/DevSecOps-Pipeline-Project/actions/runs/23408820215) |
| Security Reporting & Alerts | [View Log](https://github.com/achyutananddalpati/DevSecOps-Pipeline-Project/actions/runs/23409160018) |

---

## 📊 Security Assessment Reports

| Report | Link |
|---|---|
| SonarQube Vulnerability Report | [View on SonarCloud](https://sonarcloud.io/project/overview?id=achyutananddalpati_DevSecOps-Pipeline-Project) |
| OWASP ZAP Full Vulnerability Report | [Download Artifact](https://github.com/achyutananddalpati/DevSecOps-Pipeline-Project/actions/runs/23407035447/artifacts/6047678616) |
| Nmap Scan Report | [Download Artifact](https://github.com/achyutananddalpati/DevSecOps-Pipeline-Project/actions/runs/23406930949/artifacts/6047419901) |
| Service Identification Report | [Download Artifact](https://github.com/achyutananddalpati/DevSecOps-Pipeline-Project/actions/runs/23406971607/artifacts/6047435186) |
| TruffleHog Secret Scanning Report | [Download Artifact](https://github.com/achyutananddalpati/DevSecOps-Pipeline-Project/actions/runs/23407006481/artifacts/6047442068) |
| Automated Exploit Report | [Download Artifact](https://github.com/achyutananddalpati/DevSecOps-Pipeline-Project/actions/runs/23408820215/artifacts/6048010888) |

---

## 👤 Author

**Achyutanand Dalpati**
Bachelor of Computer Applications (Specialization — Cloud & Security)
Amity University Online, Noida, Uttar Pradesh

> *"Security is not a product, but a process."*

**Project Guide:** Harendra Pratap Singh — Senior Application Developer, Accenture Solutions Pvt Ltd, Gurugram

---

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-❤️%20and%20Security-red?style=flat-square"/>
  <img src="https://img.shields.io/badge/Status-Completed-brightgreen?style=flat-square"/>
  <img src="https://img.shields.io/github/languages/top/achyutananddalpati/DevSecOps-Pipeline-Project?style=flat-square"/>
</p>
