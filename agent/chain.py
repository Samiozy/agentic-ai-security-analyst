"""Stage 1: LLM-only narrative over real, saved scanner evidence."""
import json
from agent.prompts import CHAIN_SYSTEM

def run_chain(model, findings):
    text,usage=model.complete(CHAIN_SYSTEM,"Analyze observations:\n"+json.dumps(findings,indent=2))
    return {'stage':'chain','report':text,'usage':usage}
