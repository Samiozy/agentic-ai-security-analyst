"""Enumerate configured TCP ports; each socket connection remains lab-scoped.

This is genuine enumeration, not a simulated Nmap result. Run only on your VM.
"""
from scanners.common import tcp_connect
from schemas.finding import Finding
from guardrails.scope import check_target

def scan_ports(host: str, ports: list[int]) -> list[dict]:
    output = []
    for port in ports:
        check_target(host,port)  # authorization FIRST, even if socket fails
        try:
            with tcp_connect(host,port):
                output.append(Finding(f"{host}:{port}","port_scan","open_tcp_port",
                    f"TCP port {port} accepts connections",f"TCP connect to {host}:{port} succeeded").to_dict())
        except (OSError,TimeoutError) as exc:
            output.append(Finding(f"{host}:{port}","port_scan","closed_or_filtered",
                "Connection unsuccessful",type(exc).__name__).to_dict())
    return output
