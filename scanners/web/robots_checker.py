"""Read only the /robots.txt resource of the allowlisted application."""
from urllib.parse import urlsplit, urlunsplit
from scanners.common import safe_request
from guardrails.scope import check_url
from schemas.finding import Finding

def check_robots(url: str) -> list[dict]:
    check_url(url)
    p=urlsplit(url)
    target=urlunsplit((p.scheme,p.netloc,"/robots.txt","",""))
    res=safe_request(target)
    disallowed=[s.strip() for s in res['body'].splitlines() if s.lower().strip().startswith('disallow:')]
    return [Finding(target,"robots_txt","robots_metadata",
        "Robots directives discovered; not automatically a vulnerability",
        f"HTTP {res['status']}; directives={disallowed[:15]}").to_dict()]
