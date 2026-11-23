# Architecture and trust boundaries

1. **Allowed lab**: locally isolated Metasploitable 2 service VM and localhost
   OWASP Juice Shop application.
2. **Python recon functions**: each performs a non-exploitative check after
   enforcing the exact IP/port allowlist.
3. **MCP server**: exposes six functions to an MCP client/agent.
4. **Model stages**: Chain (no KB), Retrieval (local KB with citations), and
   Agent (proposes one MCP call; approved human executes).
5. **Trust controls**: agent suggestions and retrieved content are untrusted;
   agent actions and scanner functions both validate scope. No follow-on actions
   without a new typed `APPROVE`.
6. **Evaluation**: same evidence across stages/models, manual grounding review,
   trace of refused out-of-scope requests, timing and cost comparison.

See the comprehensive Mermaid graph in the root README for the architectural
layout and the demonstration sequence.
