# SSH Honeypot Defensive Exercises

A cybersecurity capstone project investigating potential SSH attack patterns and defensive control effectiveness through honeypot deployment in a fully closed laboratory environment.

> ** Educational Use Only**
> All scripts and configurations in this repository are intended for use in isolated, controlled laboratory environments only. Do not run these scripts against systems you do not own or do not have explicit written permission to test.

---

## Project Overview

This project deploys a Cowrie SSH honeypot in an isolated VirtualBox network and executes three categories of simulated attack against it. Multiple defensive controls are then applied and tested to evaluate their effectiveness. The complete findings — including the discovery that Docker silently bypasses host firewall rules — are documented in the accompanying paper.

**Key finding:** Conventional host-level firewall rules (UFW, iptables INPUT chain) do not protect Docker-deployed services. Effective container traffic restriction requires rules placed in the DOCKER-USER chain.

---

## Lab Architecture

| Component | Specification |
|---|---|
| Virtualization | VirtualBox with host-only network adapter |
| VM 1 (Honeypot) | Ubuntu 22.04 LTS Server, 192.168.56.10 |
| VM 2 (Attacker) | Kali Linux, 192.168.56.20 |
| Honeypot Software | Cowrie SSH honeypot (Docker deployment) |
| Network | Fully isolated — no internet routing |

---

## Repository Contents

```
.
├── README.md                          This file
├── scripts/
│   ├── scenario_a_spray.py           Credential spray attack
│   ├── scenario_b_recon.py           Post-authentication reconnaissance
│   └── scenario_c_payload.py         Payload delivery simulation

```

---

## Quick Start

### Prerequisites

- VirtualBox installed on your local machine
- Ubuntu 22.04 LTS Server ISO
- Kali Linux VirtualBox appliance
- Approximately 8 GB free RAM and 40 GB free disk space

### Deploying the Honeypot (VM 1)

```bash
# Install Docker
sudo apt-get update && sudo apt-get install -y docker.io
sudo systemctl start docker && sudo systemctl enable docker

# Deploy Cowrie
sudo docker run -d --name cowrie --restart unless-stopped \
  -p 22:2222 -p 23:2223 \
  -v /opt/cowrie/logs:/home/cowrie/cowrie/var/log/cowrie \
  -v /opt/cowrie/dl:/home/cowrie/cowrie/var/lib/cowrie/downloads \
  cowrie/cowrie:latest

# Verify deployment
sudo docker ps
```

### Preparing the Attacker (VM 2)

```bash
# Install dependencies
sudo apt-get install -y sshpass
pip3 install paramiko

# Verify connectivity to honeypot
ping 192.168.56.10
```

### Running the Attack Scenarios

```bash
# Run each scenario from Kali
python3 scripts/scenario_a_spray.py
python3 scripts/scenario_b_recon.py
python3 scripts/scenario_c_payload.py
```

For Scenario C, start a local HTTP server first to host the placeholder payload:

```bash
echo "SIMULATED_PAYLOAD" > /tmp/malware.sh
cd /tmp && python3 -m http.server 8080
```

### Extracting Logs

```bash
# From VM 1
sudo docker logs cowrie 2>&1 | sudo tee ~/cowrie_data.txt
wc -l ~/cowrie_data.txt
```

---

## Defensive Controls Tested

The project applied five defensive controls in sequence:

| Phase | Control | Result |
|---|---|---|
| I | None (baseline) | All attacks logged |
| II | Fail2ban automated banning | Integration with Docker proved fragile | (FAILED)
| II | UFW rate limiting | bypassed by Docker network rules |
| II | iptables INPUT throttling | bypassed by Docker network rules |
| III | iptables DOCKER-USER chain | Complete attack blocking achieved |

### The Working Defense

```bash
# Block attacker IP via DOCKER-USER chain
sudo iptables -I DOCKER-USER -s 192.168.56.20 -j DROP

# Verify rule is loaded
sudo iptables -L DOCKER-USER -v -n

# Remove rule when finished
sudo iptables -D DOCKER-USER -s 192.168.56.20 -j DROP
```

---

## Attack Scenarios Explained

### Scenario A — Credential Spray

Simulates an automated credential stuffing attack using 20 commonly attempted username and password pairs. Connection attempts are spaced with a 0.5 second delay to mimic the throttled behavior of attack.

Credentials are drawn from publicly documented weak password lists. None of the credentials are valid on any real system.

### Scenario B — Post-Authentication Reconnaissance

Simulates a human attacker performing system enumeration after a successful login. Executes eleven reconnaissance commands including system identification, user enumeration, and process inspection. Cowrie accepts all login attempts by default, allowing this scenario to proceed through to command execution.

### Scenario C — Payload Delivery

Simulates malware delivery via wget and curl commands. The "payload" is a benign placeholder file (`SIMULATED_PAYLOAD`) served from a local HTTP server on the attacker VM. No actual malware is involved at any point in this project.

---

## Ethical and Safety Notes

- All testing was performed in a fully isolated VirtualBox host-only network with no internet routing
- No real-world systems were probed, scanned, or attacked at any point
- The "malware" file used in Scenario C contains only the string `SIMULATED_PAYLOAD` and has no malicious functionality
- All IP addresses used (192.168.56.0/24) are from RFC 5737 documentation ranges and are not routable on the public internet
- The project complies with all applicable institutional policies that are outlined by DePaul University's Syllabus.

---

## References

The full academic paper documenting the methodology, results, and findings is available [in this repository / upon request].

Key external references:
- Cowrie SSH Honeypot — https://github.com/cowrie/cowrie
- Fail2ban Documentation — https://www.fail2ban.org/
- Docker and iptables — https://docs.docker.com/network/iptables/
- NIST SP 800-123: Guide to General Server Security
- SecLists Penetration Testing Lists — https://github.com/danielmiessler/SecLists


This project is released for educational purposes

---
```
