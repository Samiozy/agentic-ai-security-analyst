# Web lab — Partner B

Run `docker compose -f labs/web_lab/compose.yaml up -d` at project root.
The OWASP Juice Shop image binds only `127.0.0.1:3000`, not `0.0.0.0`.
Confirm `http://127.0.0.1:3000` loads on your own machine. Execute
`python cli.py --mode collect --domain web --target http://127.0.0.1:3000`.
Approve each check separately. Save the observed outputs and enrich the web KB.
The probes are reconnaissance only; no exploitation is performed.

**Environment warning:** Docker image versions and headers vary; collect live
findings rather than assuming the app exhibits a particular weakness.
