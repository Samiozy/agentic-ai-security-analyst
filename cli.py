"""Command-line demonstration and data collection.

No scanning occurs without a new typed approval; refuse other networks in code.
The deterministic `--mode evidence` run is NOT a substitute for two LLM runs.
"""
import argparse
import asyncio
import json
from pathlib import Path
from agent.chain import run_chain
from agent.retrieval import grounding,run_retrieval
from agent.security_agent import run_agent_step
from guardrails.approval import require_approval
from guardrails.scope import check_target,check_url
from models.model_factory import get_model

ROOT=Path(__file__).resolve().parent

def save(name,data):
    output=ROOT/'results'/name
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(data,indent=2),encoding='utf-8')
    print('Saved:',output)

def load_env():
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT/'.env')
    except ImportError:
        pass

async def main():
    p=argparse.ArgumentParser(description='Lab-only AI Security Analyst')
    p.add_argument('--mode',choices=['collect','evidence','chain','rag','agent'],required=True)
    p.add_argument('--domain',choices=['service','web'],default='web')
    p.add_argument('--model',choices=['HOSTED','API'],default='HOSTED')
    p.add_argument('--target',help='literal service host IP or full web URL')
    p.add_argument('--ports',default='21,22,80')
    p.add_argument('--objective',default='Inspect approved lab using a safe non-exploitative scanner')
    args=p.parse_args()
    load_env()
    if args.mode=='agent':
        result=await run_agent_step(get_model(args.model),args.objective)
        save('reports/agent_step.json',result)
        print(json.dumps(result,indent=2));return
    if args.mode=='collect':
        if not args.target: p.error('--target required for collect')
        if args.domain=='service':
            from scanners.service.port_scanner import scan_ports
            from scanners.service.banner_grabber import grab_banner
            from scanners.service.ftp_checker import check_anonymous_ftp
            ports=[int(x) for x in args.ports.split(',')]
            for port in ports: check_target(args.target,port)
            if not require_approval(f'Scan {args.target} TCP ports {ports}'): return
            findings=scan_ports(args.target,ports)
            if 21 in ports:
                if require_approval(f'Check anonymous FTP on {args.target}:21'):
                    findings+=check_anonymous_ftp(args.target,21)
                if require_approval(f'Read FTP banner on {args.target}:21'):
                    findings+=grab_banner(args.target,21)
            file='service_scans/live_findings.json'
        else:
            from scanners.web.security_headers import check_security_headers
            from scanners.web.http_methods import check_http_methods
            from scanners.web.robots_checker import check_robots
            check_url(args.target)
            findings=[]
            for label,func in [('security headers',check_security_headers),('HTTP methods',check_http_methods),('robots.txt',check_robots)]:
                if require_approval(f'Inspect {label} on {args.target}'):
                    findings+=func(args.target)
            file='web_scans/live_findings.json'
        save(file,findings)
        print(json.dumps(findings,indent=2));return
    file='service_scans/live_findings.json' if args.domain=='service' else 'web_scans/live_findings.json'
    path=ROOT/'results'/file
    if not path.exists(): p.error('Collect real findings first: '+str(path))
    findings=json.loads(path.read_text(encoding='utf-8'))
    if args.mode=='evidence':
        result=grounding(findings)
        save('reports/'+args.domain+'_candidates.json',result)
    else:
        model=get_model(args.model)
        result=run_chain(model,findings) if args.mode=='chain' else run_retrieval(model,findings)
        save(f'reports/{args.domain}_{args.mode}_{args.model.lower()}.json',result)
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    asyncio.run(main())
