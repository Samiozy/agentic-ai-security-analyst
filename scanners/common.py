"""Network primitives shared by real (non-exploitative) lab scanners."""
import socket
import urllib.error
import urllib.request
from guardrails.scope import ScopeError, check_target, check_url

class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Disallow following Location headers to potentially out-of-scope hosts."""
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise ScopeError(f"Redirect denied (not followed): HTTP {code}")

def safe_request(url: str, method="GET", timeout=4):
    check_url(url)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect)
    req = urllib.request.Request(url, method=method, headers={"User-Agent":"course-lab-audit/1.0"})
    try:
        with opener.open(req, timeout=timeout) as r:
            return {"status":r.status,"headers":dict(r.headers),"body":r.read(2048).decode("utf-8","replace")}
    except urllib.error.HTTPError as e:
        # 3xx redirects are never followed. 4xx responses still include valid evidence.
        return {"status":e.code,"headers":dict(e.headers),"body":""}

def tcp_connect(host, port, timeout=1.5):
    check_target(host,port)
    return socket.create_connection((host,int(port)),timeout=timeout)
