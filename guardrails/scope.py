"""Fail-closed network scope: validate every destination before any connection.

Do not accept user-controlled DNS hosts: exact IP addresses are required. This
prevents DNS rebinding and redirects to an unintended machine. Allowlisted ports
and IPs are read once from project configuration (no permissive defaults).
"""
import ipaddress
import json
from pathlib import Path
from urllib.parse import urlsplit

class ScopeError(ValueError):
    """Requested network destination is outside the instructor-approved lab."""

CONFIG = Path(__file__).with_name("targets.json")

def _config():
    if not CONFIG.is_file():
        raise ScopeError("No scope configuration; refusing all network actions")
    obj = json.loads(CONFIG.read_text())
    if not isinstance(obj.get("targets"), list) or not obj["targets"]:
        raise ScopeError("No authorized targets configured")
    return obj["targets"]

def check_target(host: str, port: int) -> tuple[str, int]:
    """Accept only explicitly listed literal IP addresses plus enumerated ports."""
    try:
        addr = ipaddress.ip_address(host)
        p = int(port)
        if isinstance(port, bool) or not 1 <= p <= 65535:
            raise ValueError("invalid port")
    except (ValueError, TypeError) as exc:
        raise ScopeError("Target must be a literal IPv4/IPv6 address with valid port") from exc
    for entry in _config():
        if str(addr) == entry.get("ip") and p in entry.get("ports", []):
            if not (addr.is_private or addr.is_loopback or addr.is_link_local):
                raise ScopeError("Public network addresses are not permitted")
            return str(addr), p
    raise ScopeError(f"DENIED: {addr}:{p} is not on the exact lab allowlist")

def check_url(url: str) -> tuple[str, int, str]:
    parsed = urlsplit(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
        raise ScopeError("Only absolute HTTP(S) URLs without credentials/fragments are allowed")
    try:
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
    except ValueError as exc:
        raise ScopeError("Invalid port") from exc
    host, port = check_target(parsed.hostname, port)
    return host, port, parsed.scheme
