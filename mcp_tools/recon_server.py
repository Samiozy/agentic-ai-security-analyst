"""One real MCP server exposing exactly three scanners per security domain.

Scope enforcement happens inside scanner functions, not only on the agent side.
Run from final_project/: python -m mcp_tools.recon_server
"""
from mcp.server.fastmcp import FastMCP
from guardrails.tool_authorization import consume_approval
from scanners.service.port_scanner import scan_ports as _scan_ports
from scanners.service.banner_grabber import grab_banner as _grab_banner
from scanners.service.ftp_checker import check_anonymous_ftp as _ftp
from scanners.web.security_headers import check_security_headers as _headers
from scanners.web.http_methods import check_http_methods as _methods
from scanners.web.robots_checker import check_robots as _robots

mcp=FastMCP('lab-security-analyst',log_level='WARNING')

@mcp.tool()
def scan_ports(host: str, ports: list[int], approval_token: str) -> list[dict]:
    """Identify TCP ports open on the exact approved lab host and port allowlist."""
    consume_approval(approval_token,"scan_ports",{'host':host,'ports':ports})
    return _scan_ports(host,ports)

@mcp.tool()
def grab_banner(host: str, port: int, approval_token: str) -> list[dict]:
    """Read the greeting from one approved TCP service; no authentication."""
    consume_approval(approval_token,"grab_banner",{'host':host,'port':port})
    return _grab_banner(host,port)

@mcp.tool()
def check_anonymous_ftp(host: str, port: int, approval_token: str) -> list[dict]:
    """Check whether approved lab FTP accepts an anonymous login (read-only)."""
    consume_approval(approval_token,"check_anonymous_ftp",{'host':host,'port':port})
    return _ftp(host,port)

@mcp.tool()
def check_security_headers(url: str, approval_token: str) -> list[dict]:
    """Fetch response headers and find missing browser protections on local web lab."""
    consume_approval(approval_token,"check_security_headers",{'url':url})
    return _headers(url)

@mcp.tool()
def check_http_methods(url: str, approval_token: str) -> list[dict]:
    """Send a single OPTIONS request to an approved web lab URL."""
    consume_approval(approval_token,"check_http_methods",{'url':url})
    return _methods(url)

@mcp.tool()
def check_robots(url: str, approval_token: str) -> list[dict]:
    """Fetch /robots.txt from an approved web lab without crawling or fuzzing."""
    consume_approval(approval_token,"check_robots",{'url':url})
    return _robots(url)

if __name__=='__main__':
    mcp.run(transport='stdio')
