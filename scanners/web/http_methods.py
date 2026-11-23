"""Single OPTIONS request; reports Allow header without sending unsafe verbs."""
from scanners.common import safe_request
from schemas.finding import Finding

def check_http_methods(url: str) -> list[dict]:
    resp=safe_request(url,method="OPTIONS")
    allowed=next((v for k,v in resp["headers"].items() if k.lower()=="allow"),"")
    return [Finding(url,"http_methods","advertised_http_methods",
        "Server response to OPTIONS (not a proof methods are usable)",
        f"HTTP {resp['status']}; Allow: {allowed or '(not advertised)'}").to_dict()]
