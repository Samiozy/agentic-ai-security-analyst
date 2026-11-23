"""One-time host-issued approvals for MCP subprocess tool calls.

An MCP client could bypass the notebook UI. Therefore each MCP tool itself
requires a short-lived approval token that matches the exact tool + arguments.
Only the trusted local runner creates a token AFTER typed human approval.
These tokens are NOT exposed as model choices or environment secrets.
"""
import hashlib
import json
import os
from pathlib import Path
import secrets
import tempfile
import time

DIR = Path(tempfile.gettempdir()) / f"course_lab_approvals_{os.getuid()}"

def digest(tool, args):
    return hashlib.sha256(json.dumps({'tool':tool,'args':args},sort_keys=True,separators=(',',':')).encode()).hexdigest()

def mint_approval(tool, args):
    """Call only from the human-approval-controlled runner."""
    DIR.mkdir(mode=0o700,parents=True,exist_ok=True)
    os.chmod(DIR,0o700)
    token=secrets.token_urlsafe(32)
    path=DIR/(token+'.json')
    content=json.dumps({'digest':digest(tool,args),'expires':time.time()+60})
    with path.open('x') as f: f.write(content)
    os.chmod(path,0o600)
    return token

def consume_approval(token,tool,args):
    if not isinstance(token,str) or len(token)>128 or not token or any(ch not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-' for ch in token):
        raise PermissionError('MCP action refused: invalid approval token')
    path=DIR/(token+'.json')
    try:
        # One-time consume: delete the token before authorizing the action.
        content=json.loads(path.read_text())
        path.unlink()
    except (OSError,ValueError) as exc:
        raise PermissionError('MCP action refused: approval missing or already consumed') from exc
    if content.get('digest')!=digest(tool,args) or time.time()>content.get('expires',0):
        raise PermissionError('MCP action refused: approval does not match action or has expired')
    return True
