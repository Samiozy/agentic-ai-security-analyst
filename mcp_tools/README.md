# MCP integration

`recon_server.py` wraps the six real scanners using the official FastMCP SDK.
`client.py` spawns the MCP server on stdio and calls individual tools. Start a
standalone server with `python -m mcp_tools.recon_server` or use the Stage 3 CLI
which launches it as a subprocess. An agent proposes a tool and JSON parameters;
`agent/security_agent.py` rejects invalid/out-of-scope parameters and waits for
**typed APPROVE**, after which the runner mints a short-lived single-use token bound to the exact tool and parameters; the MCP server independently consumes the token and checks scope again. A client calling MCP directly cannot bypass human approval.
