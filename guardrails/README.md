# Mandatory security brakes

`scope.py` fails closed on missing/malformed config, DNS names, public addresses,
unauthorized ports and URLs. `targets.json` is a deliberately narrow lab-only
allowlist; replace the sample service IP with your actual host-only VM address.
`approval.py` requires `APPROVE` **for each individual action**. CLI approval
and MCP agent approval are distinct calls, not blanket authorization. HTTP
redirects are never followed. Test negative cases with `pytest` and demonstrate
one rejected public target plus one rejected approval in the final video.

`tool_authorization.py` binds each MCP execution to a single-use, short-lived token
created **after** typed approval. Direct clients without tokens fail closed.
