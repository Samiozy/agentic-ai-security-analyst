"""Small loopback TCP fixture verifies service scanner output is genuinely live."""
import json
import socket
import threading
from scanners.service.port_scanner import scan_ports
from scanners.service.banner_grabber import grab_banner

def test_scanners_with_live_loopback_fixture(monkeypatch,tmp_path):
    server=socket.socket()
    server.bind(('127.0.0.1',0));server.listen(3)
    host,port=server.getsockname()
    config=tmp_path/'targets.json'
    config.write_text(json.dumps({'targets':[{'ip':host,'ports':[port]}]}))
    monkeypatch.setattr('guardrails.scope.CONFIG',config)
    def worker():
        for _ in range(2):
            conn,_=server.accept()
            conn.sendall(b'220 fixture-service\r\n')
            conn.close()
    t=threading.Thread(target=worker,daemon=True);t.start()
    try:
        assert scan_ports(host,[port])[0]['category']=='open_tcp_port'
        assert '220 fixture' in grab_banner(host,port)[0]['evidence']
    finally:
        server.close();t.join(timeout=2)
