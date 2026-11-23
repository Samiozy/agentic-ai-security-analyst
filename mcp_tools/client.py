"""Call a Python MCP server over stdio using the official MCP SDK."""
import json
import sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def call_tool(name,params,approval_token):
    cwd=str(Path(__file__).resolve().parents[1])
    server=StdioServerParameters(command=sys.executable,args=['-m','mcp_tools.recon_server'],cwd=cwd)
    async with stdio_client(server) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            r=await session.call_tool(name,{**params,'approval_token':approval_token})
            return {'is_error':r.isError,'content':[getattr(c,'text',str(c)) for c in r.content]}
