"""Exercise real urllib redirect handling without making network connections."""
import ast
import io
import json
import ssl
import urllib.request
from email.message import Message
from pathlib import Path
from urllib.response import addinfourl

import pytest

from reference import recon_server_web as server


@pytest.fixture(params=["server", "notebook"])
def recon(request):
    if request.param == "server":
        return server._http_get
    path = Path(__file__).resolve().parents[1] / "reference/part3_web_pentest_real.ipynb"
    notebook = json.loads(path.read_text())
    source = next("".join(c["source"]) for c in notebook["cells"]
                  if "def http_recon(" in "".join(c["source"]))
    tree = ast.parse(source)
    # Load the actual definitions without running the notebook's live demo.
    tree.body = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))
                 or isinstance(node, ast.Assign) and any(
                     isinstance(t, ast.Name) and t.id in {"ALLOWED_HOSTS", "CACHED"}
                     for t in node.targets)]
    namespace = {"urllib": urllib, "ssl": ssl}
    exec(compile(tree, str(path), "exec"), namespace)

    def call(url):
        result = namespace["http_recon"](url)
        return result["status"], result["headers"], result["live"], result.get("error", "")
    return call


@pytest.fixture
def transport(monkeypatch):
    calls = []
    responses = []

    def http_open(self, request):
        calls.append(request.full_url)
        code, location, body = responses.pop(0)
        headers = Message()
        headers["Content-Type"] = "text/plain"
        if location:
            headers["Location"] = location
        response = addinfourl(io.BytesIO(body), headers, request.full_url, code)
        response.msg = "test response"
        return response

    monkeypatch.setattr(urllib.request.HTTPHandler, "http_open", http_open)
    monkeypatch.setattr(urllib.request, "getproxies", lambda: {})
    return calls, responses


@pytest.mark.parametrize("code", [301, 302, 303, 307, 308])
@pytest.mark.parametrize("destination", ["http://127.0.0.1:8080/private", "//unlisted.invalid/secret", "/next"])
def test_redirect_never_issues_second_request(recon, transport, code, destination):
    calls, responses = transport
    responses.append((code, destination, b""))
    result = recon("http://scanme.nmap.org")
    assert not result[2]
    assert "Redirect denied" in result[3]
    assert calls == ["http://scanme.nmap.org"]


def test_normal_response_still_live(recon, transport):
    calls, responses = transport
    responses.append((200, None, b"ordinary content"))
    status, headers, live, _ = recon("http://scanme.nmap.org")
    assert status == 200 and live
    assert headers["Content-Type"] == "text/plain"
    assert len(calls) == 1


@pytest.mark.parametrize("tool", [server.fetch_headers, server.check_security_headers, server.get_robots])
def test_mcp_entrypoints_block_redirect(tool, transport):
    calls, responses = transport
    responses.append((302, "http://127.0.0.1:8080/private", b""))
    tool("http://scanme.nmap.org/probe")
    assert len(calls) == 1


def test_robots_second_fetch_cannot_redirect(transport):
    calls, responses = transport
    responses.extend([(200, None, b""), (302, "http://127.0.0.1:8080/private", b"")])
    result = server.get_robots("http://scanme.nmap.org/probe")
    assert "Redirect denied" in result
    assert calls == ["http://scanme.nmap.org/probe/robots.txt"] * 2


def test_robots_normal_body_preserved(transport):
    calls, responses = transport
    responses.extend([(200, None, b""), (200, None, b"User-agent: *\nDisallow: /private")])
    assert "Disallow: /private" in server.get_robots("http://scanme.nmap.org")
    assert len(calls) == 2
