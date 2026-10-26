<div align="center">

# Codex-Sec

**Codex-ready security assessment skills for authorized security research, red team exercises, and vulnerability analysis.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-101-red.svg)](#skill-index)
[![Categories](https://img.shields.io/badge/categories-24-orange.svg)](#categories)
[![Stars](https://img.shields.io/github/stars/lahmidiamoumen/Codex-Sec?style=social)](https://github.com/lahmidiamoumen/Codex-Sec)
[![Forks](https://img.shields.io/github/forks/lahmidiamoumen/Codex-Sec?style=social)](https://github.com/lahmidiamoumen/Codex-Sec/network/members)

[Overview](#overview) &bull; [Quickstart](#quickstart) &bull; [Categories](#categories) &bull; [Skill Index](#skill-index) &bull; [Contributing](#contributing)

</div>

---

## Overview

`Codex-Sec` is a library of security assessment skills designed for Codex. The Codex-ready skills live in `.agents/skills/` and use the standard `SKILL.md` format, with supporting references where needed. The repository includes tools for maintaining and enhancing these Codex skills.

Each skill provides focused methodology, validation guidance, interpretation checks, and defensive acceptance criteria. Use these materials only for systems and accounts you are authorized to assess.

**Use cases:** authorized red team engagements, bug bounty triage, security research, CTF preparation, operator training, and methodical attack surface exploration.

---

## Quickstart

Clone the repository:

```sh
git clone https://github.com/lahmidiamoumen/Codex-Sec.git
cd Codex-Sec
```

### Use in this repository

The Codex-ready skills are in `.agents/skills/`. When this repository is your Codex workspace, that directory provides the skills for the project.

### Install skills globally on Windows

Copy the skill folders into your Codex user skills directory:

```powershell
$skillsRoot = Join-Path $env:USERPROFILE ".codex\skills"
New-Item -ItemType Directory -Force -Path $skillsRoot | Out-Null
Copy-Item -Path ".\.agents\skills\*" -Destination $skillsRoot -Recurse -Force
```

Codex's default user skills directory is `%USERPROFILE%\.codex\skills`; if `CODEX_HOME` is set, use its `skills` subdirectory instead.

---

## Categories

| Category | Skills | Focus |
|---|---:|---|
| [Web Application](#web-application) | 28 | OWASP Top 10, business logic, injection, browser, and cache vulnerabilities |
| [Auth & Identity](#auth--identity) | 4 | JWT, OAuth/OIDC, SAML, and session lifecycle testing |
| [Active Directory](#active-directory) | 4 | On-prem AD, AD CS, Kerberoasting, legacy accounts, and NetExec workflows |
| [Wireless](#wireless) | 14 | 802.11, WPA2/3, EAP, WPS, evil-twin, BLE, Zigbee, Z-Wave, LoRa, sub-GHz |
| [Cloud](#cloud) | 1 | AWS, Azure, GCP attack paths |
| [Mobile](#mobile) | 1 | Android and iOS application testing |
| [IoT & Embedded](#iot--embedded) | 1 | Hardware, firmware, RTOS, ICS/OT |
| [Infrastructure & Red Team](#infrastructure--red-team) | 7 | Initial access, EDR evasion, advanced red team operations, Windows internals |
| [Exploit Development](#exploit-development) | 6 | Stack/heap corruption, ROP, mitigations, crash analysis, TOCTOU |
| [Fuzzing & Vulnerability Research](#fuzzing--vulnerability-research) | 4 | libFuzzer, AFL++, coverage-guided fuzzing, vulnerability taxonomy |
| [Reconnaissance](#reconnaissance) | 3 | OSINT, structured intelligence, and dangling DNS review |
| [API Security](#api-security) | 3 | REST/gRPC/WebSocket testing, mass assignment, business logic abuse |
| [Container & Kubernetes](#container--kubernetes) | 2 | Container escape, Kubernetes cluster exploitation |
| [CI/CD & Pipeline](#cicd--pipeline) | 3 | Pipeline, secrets, and AI coding-action security |
| [Cryptography](#cryptography) | 3 | Cryptographic implementation, padding-oracle, and TLS/SSL review |
| [Reverse Engineering](#reverse-engineering) | 1 | Isolated binary and malware triage |
| [Privilege Escalation](#privilege-escalation) | 2 | Linux and Windows privilege escalation |
| [Post-Exploitation](#post-exploitation) | 3 | Lateral movement, persistence mechanisms, data exfiltration |
| [Forensics & C2](#forensics--c2) | 2 | Anti-forensics tradecraft, C2 framework operations |
| [Supply Chain](#supply-chain) | 2 | Supply chain attacks, dependency confusion |
| [Social Engineering](#social-engineering) | 2 | Phishing campaigns, physical/vishing/smishing |
| [Network Attacks](#network-attacks) | 1 | Layer 2/3 attacks, MITM, protocol poisoning |
| [AI Security](#ai-security) | 2 | Prompt injection, jailbreaks, RAG poisoning, and tool-boundary review |
| [Utility](#utility) | 2 | Fast triage checklists, professional reporting |

---

## Skill Index

### Web Application

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-sqli`](.agents/skills/offensive-sqli/SKILL.md) | SQL injection — error-based, blind, OOB, DB-specific payloads, ORM CVEs |
| [`offensive-xss`](.agents/skills/offensive-xss/SKILL.md) | Cross-site scripting — stored, reflected, DOM-based, mutation XSS |
| [`offensive-ssrf`](.agents/skills/offensive-ssrf/SKILL.md) | Server-side request forgery — cloud metadata pivots, filter bypass |
| [`offensive-ssti`](.agents/skills/offensive-ssti/SKILL.md) | Server-side template injection — engine fingerprinting, RCE chains |
| [`offensive-xxe`](.agents/skills/offensive-xxe/SKILL.md) | XML external entity — OOB exfiltration, blind XXE techniques |
| [`offensive-idor`](.agents/skills/offensive-idor/SKILL.md) | Insecure direct object references — enumeration, authorization bypass |
| [`offensive-file-upload`](.agents/skills/offensive-file-upload/SKILL.md) | File upload — extension bypass, polyglot files, webshell deployment |
| [`offensive-rce`](.agents/skills/offensive-rce/SKILL.md) | Remote code execution — command injection, deserialization chains |
| [`offensive-deserialization`](.agents/skills/offensive-deserialization/SKILL.md) | Insecure deserialization — Java, PHP, .NET gadget chains |
| [`offensive-race-condition`](.agents/skills/offensive-race-condition/SKILL.md) | Race conditions — TOCTOU, single-packet attacks, limit bypass |
| [`offensive-request-smuggling`](.agents/skills/offensive-request-smuggling/SKILL.md) | HTTP request smuggling — CL.TE, TE.CL, H2 desync |
| [`offensive-open-redirect`](.agents/skills/offensive-open-redirect/SKILL.md) | Open redirect — OAuth token theft, phishing, SSRF pivots |
| [`offensive-parameter-pollution`](.agents/skills/offensive-parameter-pollution/SKILL.md) | HTTP parameter pollution — WAF bypass, logic confusion |
| [`offensive-graphql`](.agents/skills/offensive-graphql/SKILL.md) | GraphQL — introspection abuse, batching attacks, alias-based IDOR |
| [`offensive-waf-bypass`](.agents/skills/offensive-waf-bypass/SKILL.md) | WAF bypass — encoding tricks, chunked transfer, case mutation |
| [`offensive-business-logic`](.agents/skills/offensive-business-logic/SKILL.md) | Business logic — workflow bypass, pricing abuse, multi-step chains |
| [`offensive-email-injection`](.agents/skills/offensive-email-injection/SKILL.md) | Email header injection — controlled mail-sink validation and recipient boundaries |
| [`offensive-dom-clobbering`](.agents/skills/offensive-dom-clobbering/SKILL.md) | DOM clobbering — named elements shadowing globals and affecting security-sensitive code |
| [`offensive-ldap-injection`](.agents/skills/offensive-ldap-injection/SKILL.md) | LDAP filter and bind injection — context-aware escaping and narrow validation |
| [`offensive-crlf-injection`](.agents/skills/offensive-crlf-injection/SKILL.md) | CRLF injection — response headers, response splitting, and log integrity |
| [`offensive-path-traversal`](.agents/skills/offensive-path-traversal/SKILL.md) | Path traversal and LFI — normalization, confinement, and canary-based checks |
| [`offensive-ssi`](.agents/skills/offensive-ssi/SKILL.md) | SSI/ESI injection — server-side fragment processing and trust boundaries |
| [`offensive-nosql-injection`](.agents/skills/offensive-nosql-injection/SKILL.md) | NoSQL injection — operator and type handling against synthetic records |
| [`offensive-clickjacking`](.agents/skills/offensive-clickjacking/SKILL.md) | Clickjacking — framing controls and safe interaction validation |
| [`offensive-csrf`](.agents/skills/offensive-csrf/SKILL.md) | CSRF — token, origin, cookie, and verified state-change checks |
| [`offensive-web-cache-poisoning`](.agents/skills/offensive-web-cache-poisoning/SKILL.md) | Web cache poisoning and deception — isolated cache namespaces and inert canaries |
| [`offensive-prototype-pollution`](.agents/skills/offensive-prototype-pollution/SKILL.md) | Prototype pollution — untrusted object keys and confirmed downstream effects |
| [`offensive-cors`](.agents/skills/offensive-cors/SKILL.md) | CORS — origin matching, credential behavior, preflight, and cache variation |

### Auth & Identity

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-jwt`](.agents/skills/offensive-jwt/SKILL.md) | JWT attacks — alg:none, key confusion, secret cracking, claim tampering |
| [`offensive-oauth`](.agents/skills/offensive-oauth/SKILL.md) | OAuth/OIDC — redirect URI abuse, token leakage, PKCE bypass |
| [`offensive-session-fixation`](.agents/skills/offensive-session-fixation/SKILL.md) | Session lifecycle — identifier rotation, cookie scope, and invalidation |
| [`offensive-saml`](.agents/skills/offensive-saml/SKILL.md) | SAML/SSO — signature, audience, replay, and identity-mapping checks |

### Active Directory

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-active-directory`](.agents/skills/offensive-active-directory/SKILL.md) | AD methodology — Kerberoast, ASREProast, Pre2k, ACL abuse, ADCS, and delegation |
| [`offensive-netexec`](.agents/skills/offensive-netexec/SKILL.md) | NetExec (nxc) — authorized service and authentication checks across SMB, LDAP, WinRM, and RDP |
| [`offensive-adcs`](.agents/skills/offensive-adcs/SKILL.md) | AD CS — template enrollment, CA permissions, and lab-safe ESC validation |
| [`offensive-kerberoasting`](.agents/skills/offensive-kerberoasting/SKILL.md) | Kerberoasting and AS-REP exposure — approved test identities and defender checks |

### Wireless

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-wifi`](.agents/skills/offensive-wifi/SKILL.md) | 802.11 overview — entrypoint for wireless assessments |
| [`offensive-wifi-recon`](.agents/skills/offensive-wifi-recon/SKILL.md) | Adapter configuration, monitor mode, multi-band airspace mapping |
| [`offensive-wpa2-psk`](.agents/skills/offensive-wpa2-psk/SKILL.md) | WPA2-PSK — handshake capture, PMKID extraction, hashcat cracking |
| [`offensive-wpa3-sae`](.agents/skills/offensive-wpa3-sae/SKILL.md) | WPA3-SAE — transition-mode downgrade, Dragonblood, side-channel attacks |
| [`offensive-wpa-enterprise`](.agents/skills/offensive-wpa-enterprise/SKILL.md) | 802.1X/EAP — credential relay, evil-twin RADIUS, certificate abuse |
| [`offensive-wps`](.agents/skills/offensive-wps/SKILL.md) | WPS — Pixie Dust offline attack, online PIN brute force, vendor PIN prediction |
| [`offensive-evil-twin`](.agents/skills/offensive-evil-twin/SKILL.md) | Evil twin — KARMA, Mana, captive portal credential capture, MITM |
| [`offensive-krack-fragattacks`](.agents/skills/offensive-krack-fragattacks/SKILL.md) | KRACK and FragAttacks — supplicant vulnerability testing |
| [`offensive-deauth-disassoc`](.agents/skills/offensive-deauth-disassoc/SKILL.md) | Deauthentication — targeted/broadcast frames, PMF awareness |
| [`offensive-bluetooth-ble`](.agents/skills/offensive-bluetooth-ble/SKILL.md) | Bluetooth LE — GATT enumeration, pairing downgrade, sniffing, MITM |
| [`offensive-bluetooth-classic`](.agents/skills/offensive-bluetooth-classic/SKILL.md) | Bluetooth BR/EDR — SDP probing, KNOB attack, BlueBorne, HID spoofing |
| [`offensive-zigbee-thread-matter`](.agents/skills/offensive-zigbee-thread-matter/SKILL.md) | 802.15.4 mesh — KillerBee, Touchlink commissioning abuse, ZCL injection |
| [`offensive-z-wave`](.agents/skills/offensive-z-wave/SKILL.md) | Z-Wave — S0 key derivation, S2 commissioning attacks, hub pivots |
| [`offensive-lorawan-sub-ghz`](.agents/skills/offensive-lorawan-sub-ghz/SKILL.md) | LoRaWAN and sub-GHz — ABP/OTAA attacks, KeeLoq, fixed-code replay, TPMS |

### Cloud

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-cloud`](.agents/skills/offensive-cloud/SKILL.md) | Multi-cloud — privilege escalation, IMDS abuse, cross-account pivots, CSPM evasion |

### Mobile

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-mobile`](.agents/skills/offensive-mobile/SKILL.md) | Android and iOS — Frida hooking, certificate pinning bypass, storage, biometric flaws |

### IoT & Embedded

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-iot`](.agents/skills/offensive-iot/SKILL.md) | IoT/OT — hardware interfaces, firmware extraction, RTOS, ICS protocols, MQTT/CoAP |

### Infrastructure & Red Team

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-initial-access`](.agents/skills/offensive-initial-access/SKILL.md) | Initial access — phishing payloads, drive-by delivery, supply chain vectors (TA0001) |
| [`offensive-advanced-redteam`](.agents/skills/offensive-advanced-redteam/SKILL.md) | Full kill chain — C2 infrastructure, OPSEC, lateral movement, persistence |
| [`offensive-edr-evasion`](.agents/skills/offensive-edr-evasion/SKILL.md) | EDR evasion — userland unhooking, indirect syscalls, PPID spoofing |
| [`offensive-shellcode`](.agents/skills/offensive-shellcode/SKILL.md) | Shellcode — writing, encoding, injection techniques, position-independent code |
| [`offensive-keylogger-arch`](.agents/skills/offensive-keylogger-arch/SKILL.md) | Input capture — keylogger architecture, hooking mechanisms |
| [`offensive-windows-mitigations`](.agents/skills/offensive-windows-mitigations/SKILL.md) | Windows mitigations — ACG, CIG, CFG, CET bypass techniques |
| [`offensive-windows-boundaries`](.agents/skills/offensive-windows-boundaries/SKILL.md) | Windows boundary defeat — sandbox escape, integrity level bypass |

### Exploit Development

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-exploit-development`](.agents/skills/offensive-exploit-development/SKILL.md) | Exploit development — stack/heap corruption, ROP chains, mitigation bypass |
| [`offensive-exploit-dev-course`](.agents/skills/offensive-exploit-dev-course/SKILL.md) | Structured exploit development curriculum |
| [`offensive-basic-exploitation`](.agents/skills/offensive-basic-exploitation/SKILL.md) | Linux binary exploitation — beginner to intermediate, mitigations disabled |
| [`offensive-crash-analysis`](.agents/skills/offensive-crash-analysis/SKILL.md) | Crash triage — exploitability assessment, root-cause analysis |
| [`offensive-mitigations`](.agents/skills/offensive-mitigations/SKILL.md) | Modern mitigations — ASLR, CFG, CET, PAC analysis and bypass |
| [`offensive-toctou`](.agents/skills/offensive-toctou/SKILL.md) | TOCTOU race conditions — binary, kernel, web, and container contexts |

### Reverse Engineering

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-reverse-engineering`](.agents/skills/offensive-reverse-engineering/SKILL.md) | Binary reverse engineering and malware triage — isolated, reproducible static and dynamic analysis |

### Fuzzing & Vulnerability Research

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-fuzzing`](.agents/skills/offensive-fuzzing/SKILL.md) | Fuzzing — libFuzzer, AFL++, coverage-guided strategies, mutation engines |
| [`offensive-fuzzing-course`](.agents/skills/offensive-fuzzing-course/SKILL.md) | Vulnerability discovery through fuzzing — structured curriculum |
| [`offensive-bug-identification`](.agents/skills/offensive-bug-identification/SKILL.md) | Bug identification — code review patterns, static analysis triggers |
| [`offensive-vuln-classes`](.agents/skills/offensive-vuln-classes/SKILL.md) | Vulnerability taxonomy — real-world examples, classification frameworks |

### Reconnaissance

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-osint`](.agents/skills/offensive-osint/SKILL.md) | OSINT tooling — recon-ng, theHarvester, Maltego, Spiderfoot, and public-channel analysis |
| [`offensive-osint-methodology`](.agents/skills/offensive-osint-methodology/SKILL.md) | OSINT methodology — structured intelligence collection and analysis |
| [`offensive-subdomain-takeover`](.agents/skills/offensive-subdomain-takeover/SKILL.md) | Dangling DNS and service references — passive verification before any claim test |

### API Security

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-api-security`](.agents/skills/offensive-api-security/SKILL.md) | API testing — OWASP API Top 10, BOLA, BFLA, mass assignment, rate limiting |
| [`offensive-api-abuse`](.agents/skills/offensive-api-abuse/SKILL.md) | API business logic — endpoint chaining, batching abuse, webhook hijacking |
| [`offensive-mass-assignment`](.agents/skills/offensive-mass-assignment/SKILL.md) | Mass assignment — DTO allowlists and independent persistence verification |

### Container & Kubernetes

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-container-escape`](.agents/skills/offensive-container-escape/SKILL.md) | Container breakout — privileged mode, Docker socket, capabilities, runc CVEs |
| [`offensive-k8s-attacks`](.agents/skills/offensive-k8s-attacks/SKILL.md) | Kubernetes attacks — RBAC abuse, etcd access, kubelet API, pod escape, CRD exploitation |

### CI/CD & Pipeline

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-cicd-pipeline`](.agents/skills/offensive-cicd-pipeline/SKILL.md) | CI/CD exploitation — GitHub Actions injection, Jenkins RCE, GitLab CI abuse |
| [`offensive-cicd-secrets`](.agents/skills/offensive-cicd-secrets/SKILL.md) | CI/CD secrets — environment variable extraction, vault misconfigs, runner token abuse |
| [`offensive-claude-code-action`](.agents/skills/offensive-claude-code-action/SKILL.md) | Claude Code Action security — untrusted PR input, token scope, and tool permissions |

### Cryptography

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-crypto-attacks`](.agents/skills/offensive-crypto-attacks/SKILL.md) | Cryptographic attacks — padding oracle, ECB manipulation, hash extension, weak PRNG |
| [`offensive-tls-attacks`](.agents/skills/offensive-tls-attacks/SKILL.md) | TLS/SSL attacks — POODLE, DROWN, Heartbleed, pinning bypass, 0-RTT replay |
| [`offensive-padding-oracle`](.agents/skills/offensive-padding-oracle/SKILL.md) | CBC padding-oracle review — synthetic ciphertexts and distinguishable failures |

### Privilege Escalation

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-linux-privesc`](.agents/skills/offensive-linux-privesc/SKILL.md) | Linux privilege escalation — SUID, capabilities, sudo, cron, kernel exploits |
| [`offensive-windows-privesc`](.agents/skills/offensive-windows-privesc/SKILL.md) | Windows privilege escalation — Potato family, service misconfigs, DLL hijacking, UAC bypass |

### Post-Exploitation

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-lateral-movement`](.agents/skills/offensive-lateral-movement/SKILL.md) | Lateral movement — PTH, PTT, NTLM relay, WMI/WinRM/DCOM, tunneling |
| [`offensive-persistence`](.agents/skills/offensive-persistence/SKILL.md) | Persistence — registry, scheduled tasks, WMI subscriptions, ticket forgery, PAM backdoors |
| [`offensive-data-exfiltration`](.agents/skills/offensive-data-exfiltration/SKILL.md) | Data exfiltration — DNS/HTTPS/ICMP tunneling, cloud staging, steganography |

### Forensics & C2

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-anti-forensics`](.agents/skills/offensive-anti-forensics/SKILL.md) | Anti-forensics — log manipulation, timestomping, ADS abuse, memory cleanup |
| [`offensive-c2-frameworks`](.agents/skills/offensive-c2-frameworks/SKILL.md) | C2 tradecraft — Cobalt Strike, Sliver, Mythic, Havoc, redirectors, domain fronting |

### Supply Chain

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-supply-chain`](.agents/skills/offensive-supply-chain/SKILL.md) | Supply chain attacks — dependency confusion, typosquatting, build system compromise |
| [`offensive-dependency-confusion`](.agents/skills/offensive-dependency-confusion/SKILL.md) | Dependency confusion — npm/PyPI/NuGet/Maven namespace attacks, safe PoC methodology |

### Social Engineering

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-phishing`](.agents/skills/offensive-phishing/SKILL.md) | Phishing — GoPhish, EvilGinx2, payload delivery, email authentication bypass |
| [`offensive-social-engineering`](.agents/skills/offensive-social-engineering/SKILL.md) | Social engineering — pretexting, vishing, smishing, physical SE, USB drops |

### Network Attacks

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-network-attacks`](.agents/skills/offensive-network-attacks/SKILL.md) | Network layer attacks — ARP spoofing, LLMNR/NBT-NS poisoning, VLAN hopping, MITM |

### AI Security

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-ai-security`](.agents/skills/offensive-ai-security/SKILL.md) | AI/ML security — prompt injection, jailbreaking, RAG poisoning, model extraction |
| [`offensive-prompt-injection`](.agents/skills/offensive-prompt-injection/SKILL.md) | Prompt injection — model/tool boundaries with synthetic canaries and mock tools |

### Utility

`.agents/skills/`

| Skill | Description |
|---|---|
| [`offensive-fast-checking`](.agents/skills/offensive-fast-checking/SKILL.md) | Rapid, rate-limited triage — high-signal checks within explicit scope |
| [`offensive-reporting`](.agents/skills/offensive-reporting/SKILL.md) | Professional reporting — CVSS scoring, evidence standards, executive summaries |

---

## Contributing

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the skill template, frontmatter standard, and review process. Focused, single-surface skills are preferred over monolithic overviews.

## License

[MIT](LICENSE) — use freely, attribution appreciated.

## Acknowledgements

- **Original Checklists:** [Sahar Shlichov](https://github.com/sahar042/offensive-checklist) — the offensive checklist collection that many of these skills build on
- **Community:** Pull requests and feedback that keep the library aligned with the evolving threat landscape

---

<div align="center">

*Purpose-built skills give Codex focused guidance for authorized security assessment work.*

[GitHub repository](https://github.com/lahmidiamoumen/Codex-Sec)

</div>
