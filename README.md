# NetSentinel: AI-Driven Network Reinforcement

**NetSentinel** is a high-performance network security auditing and automated remediation tool designed for the **Slingshot Hackathon 2026**. It combines a high-speed **Java** scanning engine with a **Python-based AI orchestrator** to identify and fix critical system vulnerabilities across an entire server subnet in real-time.

---

## 🎯 Target Environment

- **Exclusive Server Support**: This tool is designed solely for Linux-based servers and is not intended for desktop or workstation environments.
- **Remote Management**: The system assumes the presence of an SSH daemon (sshd) on all target nodes for telemetry collection and remediation.
- **Privileged Access**: The "Master Function" requires high-level (sudo) access to execute security hardening commands on the remote servers.

---

## 🚀 Features

- **High-Speed Discovery**: Utilizes a multi-threaded Java engine with custom rate limiting and a ThreadPoolExecutor to scan IPs and ports concurrently.
- **Deep Telemetry Collection**: Logs into discovered hosts via SSH to gather 10+ security metrics, including firewall status, root login configurations, and world-writable files.
- **AI-Powered Analysis**: Leverages the Gemini 1.5 Flash model to analyze server states and prioritize remediation based on a severity hierarchy.
- **Automated Remediation**: Automatically applies pre-approved security patches and configuration hardening through a modular action executor.

---

## 🛠️ System Architecture

The project follows a "Scan -> Collect -> Analyze -> Fix" lifecycle managed by a central MainFunction:

1.  **JavaScanner**: Executes the Java engine to perform raw socket-level discovery and banner grabbing.
2.  **SystemCollector**: Uses high-level network access to pull detailed telemetry from remote Linux nodes, checking for issues like empty passwords and insecure services.
3.  **SecurityAnalyzer**: Interfaces with the Gemini API to detect risks and recommend specific actions.
4.  **ActionExecutor**: Runs non-interactive sudo commands to harden the target systems based on AI recommendations.

---

## 🔒 Security & Policy

To ensure safety during automated remediation, NetSentinel employs a strict Policy Filter:

- **Whitelisted Actions**: Only pre-approved commands (e.g., secure_ssh, enable_firewall) can be executed by the AI.
- **Credential Protection**: API keys and SSH credentials are managed via environment variables and local keys, ensuring no sensitive data is stored in the source code.

---

## ⚙️ Setup & Usage

### 1. Requirements

- Ubuntu 22.04 LTS or newer
- Java 17+ (for the scanner engine)
- Python 3.10+ (for the orchestrator)
- Gemini API Key

### 2. Environment Setup

export GEMINI_API_KEY='your_api_key_here'

pip install google-genai paramiko

### 3. Compilation & Execution

Compile the Java source and run the master pipeline:

javac src/\*.java -d out

java -cp out Main <subnet-cidr>

python main.py

---

## ⚖️ License

This project was developed for the Slingshot Hackathon 2026 under the MIT License.
