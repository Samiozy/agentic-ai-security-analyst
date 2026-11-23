# Six independent Python scanning tools

**Service / Partner A:** `port_scanner.py` makes scoped TCP connections;
`banner_grabber.py` reads greetings; `ftp_checker.py` attempts one anonymous FTP
login without touching files. **Web / Partner B:** `security_headers.py` examines
HTTP headers; `http_methods.py` submits OPTIONS; `robots_checker.py` reads
robots.txt. All return the same `Finding` dictionaries, and every actual
connection checks `guardrails/scope.py` first. No exploitation, brute force or
internet scanning is implemented. For MCP tool discovery see `mcp_tools/`.
