# Evaluation plan

Compare **Chain, Retrieval and Agent** on the SAME lab observations (grounded
claims, unsupported claims, effort, autonomy and safety). Separately compare
hosted and paid-API models on identical prompts and settings (accuracy reviewed
by humans, response time, actual billed cost, and where findings are transmitted).
`coverage.py` counts ONLY manually verified grounded claims, never automatically
assumes lexical retrieval proves ground truth. Write per-finding reviewer notes
and final percentages to `results/metrics/` after live runs. Do not invent data.
