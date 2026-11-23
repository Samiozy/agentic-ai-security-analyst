"""Read the provided instructor knowledge bases plus short local-tool guidance."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def read_sections():
    docs=[]
    for p in (ROOT/'cve_knowledge_base.md',ROOT/'web_security_kb.md',ROOT/'scanner_guidance.md'):
        if not p.exists(): continue
        text=p.read_text(encoding='utf-8')
        for raw in text.split('\n# '):
            chunk=raw.strip().lstrip('#').strip()
            if chunk:
                docs.append({'source':p.name,'title':chunk.splitlines()[0].strip(),'text':chunk})
    return docs
