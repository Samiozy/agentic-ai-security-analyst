"""Report observed missing browser defenses (not proof of exploitation)."""
from scanners.common import safe_request
from schemas.finding import Finding

EXPECTED = ("content-security-policy","x-content-type-options","x-frame-options","referrer-policy")
def check_security_headers(url: str) -> list[dict]:
    resp = safe_request(url)
    headers = {k.lower():v for k,v in resp["headers"].items()}
    results=[]
    for name in EXPECTED:
        if name not in headers:
            results.append(Finding(url,"security_headers","missing_"+name.replace("-","_"),
                f"Missing HTTP response header: {name}",f"HTTP {resp['status']}; {name} absent", "low").to_dict())
    if not results:
        results.append(Finding(url,"security_headers","headers_present",
            "All checked header names observed",f"HTTP {resp['status']}").to_dict())
    return results
