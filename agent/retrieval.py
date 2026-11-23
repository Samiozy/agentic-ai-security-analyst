"""Stage 2: transparent local BM25-like token retrieval (zero external embedding API).

Search uses lexical overlap and returns citations with document headings. This is
retrieval-augmented generation, not an embedding search; upgrade optional.
"""
import json
import re
from collections import Counter
from knowledge_base.loader import read_sections
from agent.prompts import RAG_SYSTEM

def tokens(text):
    return set(re.findall(r'[a-z0-9][a-z0-9_.-]+',text.lower()))

def retrieve(query,top_k=3):
    terms=tokens(query)
    scored=[]
    for doc in read_sections():
        heading=tokens(doc['title'])
        body=tokens(doc['text'])
        score=3*len(terms & heading)+len(terms & body)
        if score:
            scored.append((score,doc))
    return [doc for _,doc in sorted(scored,key=lambda p:-p[0])[:top_k]]

def grounding(findings):
    result=[]
    for f in findings:
        query=f['category'].replace('_',' ')+" "+f['description']
        hits=retrieve(query)
        # Retrieval relevance is NOT proof of correct vulnerability mapping.
        result.append({'finding':f,'candidates':hits,'status':'needs_human_validation' if hits else 'gap'})
    return result

def run_retrieval(model,findings):
    evidence=grounding(findings)
    context=[{'finding':x['finding'],'documents':x['candidates']} for x in evidence]
    report,usage=model.complete(RAG_SYSTEM,'Analyze and cite these documents; explicitly name gaps:\n'+json.dumps(context,indent=2))
    return {'stage':'retrieval','report':report,'usage':usage,'retrieved':evidence}
