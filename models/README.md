# Two model connectors

Both use an OpenAI-compatible `/v1/chat/completions` endpoint. Configure
`HOSTED_*` for the locally accessible, self-hosted Jetstream2 14B-class model
(Ollama or vLLM) and `API_*` for a separately paid hosted API provider in `.env`.
A remote Jetstream2 endpoint should be reached via an SSH tunnel to localhost,
not by opening the public firewall. The two backends use the same prompts and
parameters. Model keys must never be added to Git. These functions make real
requests; they intentionally do not generate fake stand-in model answers.
