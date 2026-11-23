"""Measure identical prompts across live models: latency and token usage.

Pricing is provider-specific; record cost only from actual current billing.
"""
import time

def compare_models(models,system,prompt):
    results=[]
    for name,model in models.items():
        start=time.perf_counter()
        report,usage=model.complete(system,prompt)
        results.append({'model':name,'seconds':round(time.perf_counter()-start,3),
                        'usage':usage,'report':report,'cost_usd':None,
                        'cost_note':'Enter actual billed API cost; self-hosted hardware costs separate'})
    return results
