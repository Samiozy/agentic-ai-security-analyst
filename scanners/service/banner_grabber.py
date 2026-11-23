"""Read a service's unsolicited TCP greeting without authenticating/exploiting."""
from scanners.common import tcp_connect
from schemas.finding import Finding
from guardrails.scope import check_target

def grab_banner(host: str, port: int) -> list[dict]:
    check_target(host, port)
    try:
        with tcp_connect(host,port) as conn:
            conn.settimeout(2)
            data = conn.recv(512).decode("utf-8","replace").strip()
        return [Finding(f"{host}:{port}","banner_grab","service_banner",
            "Unsolicited service greeting observed",data or "(empty banner)").to_dict()]
    except (OSError,TimeoutError) as exc:
        return [Finding(f"{host}:{port}","banner_grab","banner_unavailable",
            "Banner could not be collected",str(exc)).to_dict()]
