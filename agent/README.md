# Three AI stages

- `chain.py`: same scan evidence passed to LLM without advisory retrieval;
  hypotheses must be labeled unverified.
- `retrieval.py`: deterministic lexical retrieval of the instructor KBs and
  scanner guidance, then an LLM report with cited sources and named gaps.
- `security_agent.py`: LLM chooses one MCP tool call. It cannot execute without
  scope validation AND a fresh human APPROVE; one call per step only.
- `prompts.py`: fixed prompts; scanner content is untrusted data.

The course requires comparing three approaches, not just three scripts.
Use the same underlying observations for fair Stage 1 versus Stage 2 comparison.
