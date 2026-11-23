"""Stage 3: a model proposes MCP tool calls; typed approval precedes execution.

LLM output is never executable code. The server checks exact lab scope again.
"""
import json
from agent.prompts import AGENT_SYSTEM
from guardrails.approval import require_approval
from guardrails.scope import check_target, check_url, ScopeError

TOOLS={'scan_ports','grab_banner','check_anonymous_ftp','check_security_headers','check_http_methods','check_robots'}

def validate_action(action):
    tool=action.get('tool')
    args=action.get('args')
    if tool not in TOOLS or not isinstance(args,dict):
        raise ValueError('Unknown MCP tool or malformed parameters')
    if tool=='scan_ports':
        if set(args)!= {'host','ports'} or not isinstance(args['ports'],list) or not 1<=len(args['ports'])<=12:
            raise ValueError('Invalid scan_ports arguments')
        for port in args['ports']: check_target(args['host'],port)
    elif tool in {'grab_banner','check_anonymous_ftp'}:
        if set(args)!={'host','port'}: raise ValueError('Invalid host/port arguments')
        check_target(args['host'],args['port'])
    else:
        if set(args)!={'url'}: raise ValueError('Invalid URL arguments')
        check_url(args['url'])
    return tool,args

def propose_action(model,objective):
    txt,usage=model.complete(AGENT_SYSTEM,objective)
    # Some models wrap JSON in fenced blocks; tolerate that but never eval code.
    txt=txt.strip().removeprefix('```json').removeprefix('```').removesuffix('```').strip()
    action=json.loads(txt)
    tool,args=validate_action(action)
    return {'tool':tool,'args':args,'reason':action.get('reason',''),'usage':usage}

async def run_agent_step(model,objective,*,input_fn=input):
    proposal=propose_action(model,objective)
    if not require_approval(json.dumps({'tool':proposal['tool'],'args':proposal['args']}),input_fn=input_fn):
        return {'status':'rejected','proposal':proposal}
    # MCP client call occurs only AFTER human approval and scope validation.
    from mcp_tools.client import call_tool
    from guardrails.tool_authorization import mint_approval
    approval_token=mint_approval(proposal['tool'],proposal['args'])
    result=await call_tool(proposal['tool'],proposal['args'],approval_token)
    return {'status':'executed','proposal':proposal,'tool_result':result}
