"""Offline tests for rejection guarantees and schema/KB behavior."""
import json
import threading
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
import pytest
from guardrails.scope import ScopeError,check_target,check_url
from guardrails.approval import require_approval
from agent.security_agent import validate_action
from agent.retrieval import retrieve,grounding
from scanners.web.security_headers import check_security_headers
from scanners.web.http_methods import check_http_methods
from scanners.web.robots_checker import check_robots
from schemas.finding import Finding


def test_public_ips_refused():
    with pytest.raises(ScopeError): check_target('8.8.8.8',53)
    with pytest.raises(ScopeError): check_url('https://example.com')

def test_unlisted_port_denied():
    with pytest.raises(ScopeError): check_target('127.0.0.1',22)

def test_dns_and_userinfo_denied():
    for u in ['http://localhost:3000','http://user:pass@127.0.0.1:3000',
              'http://127.0.0.1:9999','ftp://127.0.0.1:3000']:
        with pytest.raises(ScopeError):check_url(u)

def test_approval_exact_word_only():
    assert require_approval('test',input_fn=lambda _: 'APPROVE')
    for answer in ['yes','approve','APPROVE ALL','']:
        assert not require_approval('test',input_fn=lambda _:answer)

def test_agent_tool_rejection():
    with pytest.raises(ValueError):validate_action({'tool':'run_shell','args':{'command':'date'}})
    with pytest.raises(ScopeError):validate_action({'tool':'check_robots','args':{'url':'http://8.8.8.8/'}})
    with pytest.raises(ScopeError):validate_action({'tool':'scan_ports','args':{'host':'127.0.0.1','ports':[80]}})

def test_foundation_schema():
    f=Finding('127.0.0.1:3000','method','category','description','evidence')
    assert f.to_dict()['source_type']=='live'

def test_retrieval_and_grounding():
    assert any('FTP' in x['text'] for x in retrieve('Anonymous FTP enabled'))
    assert grounding([Finding('x','ftp','anonymous_ftp_enabled','Anonymous FTP enabled','login').to_dict()])[0]['status']=='needs_human_validation'

class LabHandler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def do_GET(self):
        if self.path=='/redirect':
            self.send_response(302);self.send_header('Location','http://8.8.8.8');self.end_headers();return
        self.send_response(200)
        self.send_header('Content-Type','text/plain')
        self.end_headers()
        self.wfile.write(b'User-agent: *\nDisallow: /internal\n')
    def do_OPTIONS(self):
        self.send_response(200);self.send_header('Allow','GET, OPTIONS');self.end_headers()

def test_web_scanners_local_with_temporary_allowlist(monkeypatch,tmp_path):
    server=HTTPServer(('127.0.0.1',0),LabHandler)
    host,port=server.server_address
    config=tmp_path/'targets.json'
    config.write_text(json.dumps({'targets':[{'ip':'127.0.0.1','ports':[port]}]}))
    monkeypatch.setattr('guardrails.scope.CONFIG',config)
    thread=threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    try:
        url=f'http://{host}:{port}'
        assert any(x['category']=='missing_content_security_policy' for x in check_security_headers(url))
        assert 'OPTIONS' in check_http_methods(url)[0]['evidence']
        assert '/internal' in check_robots(url)[0]['evidence']
        from scanners.common import safe_request
        from guardrails.scope import ScopeError
        with pytest.raises(ScopeError):safe_request(url+'/redirect')
    finally:
        server.shutdown();server.server_close();thread.join(timeout=2)


def test_one_time_tool_approval():
    from guardrails.tool_authorization import mint_approval, consume_approval
    args={'url':'http://127.0.0.1:3000'}
    token=mint_approval('check_robots',args)
    with pytest.raises(PermissionError):consume_approval(token,'check_http_methods',args)
    token=mint_approval('check_robots',args)
    assert consume_approval(token,'check_robots',args)
    with pytest.raises(PermissionError):consume_approval(token,'check_robots',args)
