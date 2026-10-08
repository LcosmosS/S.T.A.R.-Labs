#!/usr/bin/env python3
import argparse, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path
import fitz, requests

OLLAMA_URL='http://127.0.0.1:11434/api/generate'
DEFAULT_DOCS=['Origins.pdf','Research-Analysis+Testing.pdf','Research-Analysis+Testing_pt.2.pdf','Research-Analysis+Testing_pt.3.pdf','Branch_Rersearch-Analysis+Testing_pt.4.pdf']

def sha256(p):
    h=hashlib.sha256(); f=p.open('rb')
    for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    f.close(); return h.hexdigest()

def pages(p):
    d=fitz.open(p); out=[]; digest=sha256(p)
    for i,x in enumerate(d,start=1): out.append({'document':p.name,'sha256':digest,'page':i,'text':x.get_text('text')})
    d.close(); return out

def features(t):
    return {
      'code_like':bool(re.search(r'\b(import|from .* import|def |EllipticCurve\(|pari/gp|magma|python)\b',t,re.I)),
      'result_like':bool(re.search(r'\b(results?|output|finding|scientific finding|null result|R2|MAE|correlation|accuracy|error)\b',t,re.I)),
      'data_like':bool(re.search(r'\.(csv|fits|parquet|json)\b|\bdataset\b|\bdata source\b|\brows?\b',t,re.I)),
      'equation_like':bool(re.search(r'=|≈|∼|\\frac|\\sum|\\prod|L\(E',t))
    }

def ollama(model,prompt,temp=.1):
    r=requests.post(OLLAMA_URL,json={'model':model,'prompt':prompt,'stream':False,'options':{'temperature':temp}},timeout=600)
    r.raise_for_status(); return r.json()['response']

def extract(model,p):
    prompt=f'''You are the evidence-extraction layer of a scientific archive. Use ONLY this PDF page. Do not use outside knowledge, correct the source, or invent missing information. Return valid JSON with keys: document,page,summary,research_questions,theoretical_claims,definitions,methods,code,data_files,datasets_or_data_sources,results,errors_or_failures,interpretations,explicit_limitations,provenance_notes. Preserve exact filenames, software versions, numerical values, code fragments, and result wording where useful. Mark analogies as interpretations. If code/results continue onto another page, say so. SOURCE: {p["document"]}, page {p["page"]}\n---\n{p["text"]}\n---'''
    raw=ollama(model,prompt)
    try:return json.loads(raw)
    except Exception:return {'document':p['document'],'page':p['page'],'parse_error':True,'raw_model_output':raw}

def synthesize(model,evidence):
    data=json.dumps(evidence,ensure_ascii=False)
    prompt=f'''You are the scientific synthesis layer. Write an extremely detailed scientific paper using ONLY the supplied evidence records from these PDFs: Origins.pdf; Research-Analysis+Testing.pdf; Research-Analysis+Testing_pt.2.pdf; Research-Analysis+Testing_pt.3.pdf; Branch_Rersearch-Analysis+Testing_pt.4.pdf. Do not invent or silently correct facts. Distinguish source facts, source interpretations, proposed methods, failures, null results, and inferences. Preserve disagreements. Do not claim finite computational checks prove universal conjectures. Keep BSD-inspired analogy separate from mathematical claims about BSD. Every substantive corpus-derived claim must end with [Source: filename, p. N] or [Sources: filename, pp. N-M; other.pdf, p. K]. Reproduce source code only when actually present; identify fragmented reconstruction. Explicitly list every named data file/dataset and whether it is simulated, synthetic, or observed when the corpus says so. Structure: Title; Abstract; Provenance and Scope; Origins; Problem Formulation; Mathematical Framework; BSD Motivation; Cartographic/Cosmological Construction; Computational Program; Software; Code/Algorithms; Data and File Provenance; Experimental Design; Results; Errors and Failed Runs; Null Results/Falsification; Cross-Document Synthesis; Contradictions/Unresolved Issues; Limitations; Reproducibility; Proposed Next Experiments; Conclusion; Appendix A Code Inventory; Appendix B Data Inventory; Appendix C Page-Level Provenance. If evidence is insufficient write “not established by the supplied corpus.”\nEVIDENCE:\n{data}'''
    return ollama(model,prompt,.05)

def main():
    a=argparse.ArgumentParser(); a.add_argument('--corpus',required=True,type=Path); a.add_argument('--output',required=True,type=Path); a.add_argument('--model',required=True); a.add_argument('--docs',nargs='+',default=DEFAULT_DOCS); a.add_argument('--extract-only',action='store_true'); a.add_argument('--synthesize-only',action='store_true'); a.add_argument('--force',action='store_true'); args=a.parse_args()
    a.output.mkdir(parents=True,exist_ok=True); paths=[a.corpus/x for x in args.docs]; missing=[str(x) for x in paths if not x.exists()]
    if missing: print('Missing PDFs:\n'+'\n'.join(missing),file=sys.stderr); return 2
    ep=a.output/'page_evidence.jsonl'; mp=a.output/'corpus_manifest.json'; pp=a.output/'STAR_Scientific_Paper_v0.1.md'
    if not args.synthesize_only:
        ps=[]
        for x in paths: print('[ingest]',x.name); ps += pages(x)
        manifest={'generator':'S.T.A.R. PDF Research Ingestion & Provenance Generator v0.1','generated_at_utc':datetime.now(timezone.utc).isoformat(),'ollama_model':args.model,'ollama_endpoint':OLLAMA_URL,'documents':[{'name':x.name,'sha256':sha256(x),'bytes':x.stat().st_size,'pages':sum(y['document']==x.name for y in ps)} for x in paths]}
        mp.write_text(json.dumps(manifest,indent=2),encoding='utf8')
        evidence=[] if args.force or not ep.exists() else [json.loads(x) for x in ep.read_text(encoding='utf8').splitlines() if x.strip()]
        start=len(evidence)
        for p in ps[start:]:
            print(f'[extract] {p["document"]} p.{p["page"]}'); r=extract(args.model,p); r['_local_features']=features(p['text']); r['_sha256']=p['sha256']; evidence.append(r)
            with ep.open('w',encoding='utf8') as f:
                for z in evidence:f.write(json.dumps(z,ensure_ascii=False)+'\n')
        if args.extract_only: print('Extraction complete:',ep); return 0
    else:
        if not ep.exists(): print('Need page_evidence.jsonl first',file=sys.stderr); return 2
        evidence=[json.loads(x) for x in ep.read_text(encoding='utf8').splitlines() if x.strip()]
    print('[synthesis]',len(evidence),'page records'); paper=synthesize(args.model,evidence); pp.write_text(paper,encoding='utf8')
    (a.output/'STAR_Scientific_Paper_v0.1.json').write_text(json.dumps({'source_documents':sorted({x.get('document') for x in evidence}), 'pages':len(evidence),'paper':str(pp),'evidence_file':str(ep),'model':args.model,'source_only_policy':True},indent=2),encoding='utf8')
    print('Paper:',pp); return 0
if __name__=='__main__': raise SystemExit(main())
