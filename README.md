# Ghost-Spray

> Credential attack toolkit - password spraying, stuffing, default credentials, and hash cracking.

```
  GHOST-SPRAY  v1.0.0  |  Password Spraying & Credential Attacks
  By Gh0st-Bx1         |  github.com/Ghost-Bx1
```

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey?style=flat-square)
![Category](https://img.shields.io/badge/Category-Credential%20Attacks-red?style=flat-square)

---

## Overview

Ghost-Spray covers the full credential attack surface: one-password-at-a-time spraying with automatic lockout detection, credential stuffing from breach dumps, default credential testing for 40+ vendors, dictionary-based hash cracking with mutation rules, and a locally encrypted credential vault.

| Module     | Description                                                         |
|------------|---------------------------------------------------------------------|
| `spray`    | Password spraying - one password per round across all users         |
| `stuff`    | Credential stuffing from breach dump files                          |
| `defaults` | Default credential testing for 40+ known manufacturers             |
| `hash`     | Hash cracking via dictionary + mutation rules (MD5 to SHA-512)      |
| `vault`    | Manage the local encrypted credential vault                         |

---

## Requirements

```
Python 3.7+
No external dependencies (stdlib only)
paramiko        (optional - required for SSH spray)
```

```bash
pip install paramiko  # optional, SSH only
```

---

## Installation

```bash
git clone https://github.com/Ghost-Bx1/ghost-spray
cd ghost-spray
python ghost-spray.py --help
```

---

## Usage

### Password spray

```bash
# HTTP Basic Auth spray
python ghost-spray.py spray -t http://target.com/admin --protocol http \
    --userlist users.txt --delay 2.0

# SMTP spray with custom password list
python ghost-spray.py spray -t mail.target.com:587 --protocol smtp \
    --userlist emails.txt --passlist passwords.txt --delay 3.0 --vault-pass s3cr3t

# LDAP spray
python ghost-spray.py spray -t 192.168.1.10:389 --protocol ldap \
    --userlist users.txt --threads 5
```

### Credential stuffing

```bash
# Stuffing with breach dump
python ghost-spray.py stuff -t http://target.com/login --breach-file dump.txt

# With vault storage and JSON output
python ghost-spray.py stuff -t http://target.com/api/auth \
    --breach-file breach.json --vault-pass s3cr3t -o results.json
```

Supported breach dump formats: `user:pass`, `email:pass`, `{"email":"...","password":"..."}` JSON. Separators: `:` `;` `\t` `|`

### Default credentials

```bash
# Test web panel defaults
python ghost-spray.py defaults -t http://192.168.1.1/admin --protocol http

# Test LDAP defaults
python ghost-spray.py defaults -t 192.168.1.10:389 --protocol ldap
```

Vendors covered: D-Link, TP-Link, Netgear, Cisco, Juniper, Mikrotik, Ubiquiti, Hikvision, Dahua, VMware ESXi, Citrix, IPMI/BMC, PostgreSQL, MySQL, Redis, MongoDB, Jenkins, Tomcat, Grafana, Kibana, Jupyter, Jira, Confluence, and more.

### Hash cracking

```bash
# Crack MD5 with built-in wordlist
python ghost-spray.py hash --hash 5f4dcc3b5aa765d61d8327deb882cf99

# With custom wordlist
python ghost-spray.py hash --hash <sha256_hash> --wordlist rockyou.txt --verbose
```

Supported types: MD5 (32), SHA1 (40), SHA224 (56), SHA256 (64), SHA384 (96), SHA512 (128).

Mutation rules applied automatically: capitalization, suffixes (1, 12, 123, 2024, 2025), symbols (@, !, #), leet substitution (a->@, e->3, i->1, o->0).

### Vault management

```bash
# List saved credentials
python ghost-spray.py vault --action list --vault-pass s3cr3t

# Clear vault
python ghost-spray.py vault --action clear --vault-pass s3cr3t

# Export to JSON
python ghost-spray.py vault --action export --vault-pass s3cr3t
```

The vault stores valid credentials in `ghost-spray.vault` using XOR cipher with a SHA-256 derived key. No plaintext credentials on disk.

---

## Lockout Detection

Ghost-Spray monitors failed attempts per user. When 5 or more failures are detected within 60 seconds for the same user, it automatically pauses for 300 seconds. Use `--delay` to add additional wait time between attempts.

---

## Reference

### `spray` flags

| Flag              | Description                                              |
|-------------------|----------------------------------------------------------|
| `-t / --target`   | URL or host:port                                         |
| `--protocol`      | http, https, smtp, ldap, ssh (default: http)             |
| `--userlist`      | File with list of usernames                              |
| `--passlist`      | File with list of passwords (default: built-in list)     |
| `--delay N`       | Delay between attempts in seconds (default: 1.0)         |
| `--threads N`     | Concurrent threads per password (default: 3)             |
| `--vault-pass`    | Vault master password to store valid credentials         |
| `-o / --output`   | Save results to JSON                                     |

### `stuff` flags

| Flag              | Description                                              |
|-------------------|----------------------------------------------------------|
| `-t / --target`   | URL or host:port                                         |
| `--breach-file`   | Breach dump file (user:pass or JSON)                     |
| `--vault-pass`    | Vault master password                                    |
| `-o / --output`   | Save results to JSON                                     |

### `hash` flags

| Flag              | Description                                              |
|-------------------|----------------------------------------------------------|
| `--hash`          | Hash to crack                                            |
| `--wordlist FILE` | Custom wordlist (default: built-in)                      |
| `--verbose`       | Show each attempt                                        |

### `vault` flags

| Flag              | Description                                              |
|-------------------|----------------------------------------------------------|
| `--action`        | list, clear, or export                                   |
| `--vault-pass`    | Vault master password                                    |

## Ghost Toolkit

| Tool | Description |
|------|-------------|
| [ghost-ad](https://github.com/Ghost-Bx1/ghost-ad) | Active Directory - LDAP, Kerberoasting, AS-REP Roasting, BloodHound-lite |
| [ghost-cloud](https://github.com/Ghost-Bx1/ghost-cloud) | Cloud Security - AWS, Azure and GCP misconfiguration scanner |
| [ghost-fuzz](https://github.com/Ghost-Bx1/ghost-fuzz) | Web Fuzzing - directory brute-force, parameter fuzzing, vhost enumeration |
| [ghost-osint](https://github.com/Ghost-Bx1/ghost-osint) | OSINT - domain, email and IP intelligence from public sources |
| [ghost-privesc](https://github.com/Ghost-Bx1/ghost-privesc) | Privilege Escalation - Linux privesc checker, 17 vectors, GTFOBins |
| [ghost-recon](https://github.com/Ghost-Bx1/ghost-recon) | Reconnaissance - DNS, SSL, WAF, subdomain enumeration, email security |
| [ghost-report](https://github.com/Ghost-Bx1/ghost-report) | Reporting - pentest report generator from any ghost-* JSON output |
| [ghost-scan](https://github.com/Ghost-Bx1/ghost-scan) | Port Scanner - async TCP/UDP scanner with banner grabbing and CVE correlation |
| [ghost-shell](https://github.com/Ghost-Bx1/ghost-shell) | Payload Generation - reverse shell and web shell generator, 25+ languages |
| [ghost-spray](https://github.com/Ghost-Bx1/ghost-spray) | Credential Attacks - password spraying, stuffing, default credential testing |
| [ghost-wifi](https://github.com/Ghost-Bx1/ghost-wifi) | WiFi Attacks - monitor mode, deauth, WPA/WPA2 capture, PMKID, WPS, Evil Twin |

---

## Disclaimer

For use in authorized environments only. Penetration testing, CTF competitions, and offensive security research with explicit permission from the environment owner. Password spraying and credential stuffing without authorization are illegal. The author is not responsible for misuse.

---

**By [Gh0st-Bx1](https://github.com/Ghost-Bx1)**
