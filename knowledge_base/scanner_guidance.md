# Anonymous FTP enabled
Category: CWE-284 / OWASP A05 security misconfiguration (context-dependent). Evidence: accepted FTP anonymous login. Severity: medium when unintended. Remediation: disable anonymous access or restrict it to explicitly public directories with read-only permission. Reference: OWASP Web Security Testing Guide; NIST SP 800-123.

# Missing HTTP response header
Category: OWASP A05:2021 security misconfiguration. Evidence: observed absence of the named browser-defense header. Severity: low, context-dependent. Remediation: configure browser security headers as appropriate for the app. Reference: OWASP Secure Headers Project.

# Open TCP port
Category: attack-surface inventory, not a confirmed vulnerability. Evidence: successful TCP connection to the approved IP:port. Severity: informational. Remediation: restrict unnecessary listening services with firewall rules. Reference: NIST SP 800-123.

# Service banner
Category: service discovery / information disclosure only if unnecessary details are present. Evidence: server greeting. Severity: informational. Remediation: minimize unnecessary version disclosures; patch services based on verified vendor advisories. Reference: OWASP Web Security Testing Guide.

# HTTP methods
Category: attack surface inventory. Evidence: OPTIONS response and Allow header (if advertised). Severity: informational. Remediation: disable unnecessary methods only if verified enabled. Reference: OWASP Web Security Testing Guide.

# robots.txt metadata
Category: information exposure only if sensitive paths are independently verified. Evidence: robots.txt directives. Severity: informational. Remediation: protect sensitive resources using authentication, not robots.txt. Reference: OWASP Web Security Testing Guide.
