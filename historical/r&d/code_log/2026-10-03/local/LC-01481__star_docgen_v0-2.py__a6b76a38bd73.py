#!/usr/bin/env python3
"""S.T.A.R. Document Generator v0.2

Resumable, provenance-first PDF ingestion pipeline:
PDF -> deterministic page extraction -> bounded Ollama evidence extraction
-> evidence ledger -> bounded manuscript synthesis.

Requires: pip install pymupdf
Ollama: ollama serve && ollama pull llama3:latest
"""

from __future__ import annotations
import argparse, hashlib, json, re, sys, time, urllib.request
from pathlib import Path

try:
    import pymupdf
except ImportError:
    try: import fitz as pymupdf
    except ImportError: pymupdf = None

VERSION="0.2.0"
TYPES=("claim","definition","equation","algorithm","code","code_description",
       "dataset","experiment","result","limitation","conclusion","reference")
FILES={t:f"{t}s.jsonl" for t in TYPES}
FILES["code_description"]="code_descriptions.jsonl"

SECTIONS={
 "theory":{"claim","definition","equation","algorithm","reference"},
 "methods":{"definition","equation","algorithm","code","code_description","dataset"},
 "experiments":{"experiment","code","code_description","dataset","result"},
 "results":{"result","experiment","dataset","code"},
 "discussion":{"claim","result","limitation","conclusion","experiment"},
}

def now():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def die(s):
    raise SystemExit(s)

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def stem(s):
    return re.sub(r"[^A-Za-z0-9._-]+","_",Path(s).stem).strip("._") or "document"

def read_jsonl(p):
    if not p.exists(): return []
    out=[]
    with open(p,encoding="utf-8") as f:
        for n,line in enumerate(f,1):
            if line.strip():
                try: out.append(json.loads(line))
                except json.JSONDecodeError as e: print(f"WARNING {p}:{n}: {e}",file=sys.stderr)
    return out

def append_jsonl(p,row):
    p.parent.mkdir(parents=True,exist_ok=True)
    with open(p,"a",encoding="utf-8") as f:
        f.write(json.dumps(row,ensure_ascii=False,sort_keys=True)+"\n")

def write_json(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    q=p.with_suffix(p.suffix+".tmp")
    q.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    q.replace(p)

def parser():
    p=argparse.ArgumentParser(description="S.T.A.R. Document Generator v0.2")
    p.add_argument("--corpus",type=Path)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--model",default="llama3:latest")
    p.add_argument("--ollama-url",default="http://127.0.0.1:11434/api/generate")
    p.add_argument("--docs",nargs="*")
    g=p.add_mutually_exclusive_group()
    g.add_argument("--extract-only",action="store_true")
    g.add_argument("--analyze",action="store_true")
    g.add_argument("--resume",action="store_true")
    g.add_argument("--retry-failed",action="store_true")
    g.add_argument("--synthesize",action="store_true")
    p.add_argument("--max-pages",type=int)
    p.add_argument("--chunk-pages",type=int,default=4)
    p.add_argument("--overlap-pages",type=int,default=1)
    p.add_argument("--max-context-chars",type=int,default=18000)
    p.add_argument("--max-output-tokens",type=int,default=2500)
    p.add_argument("--request-timeout",type=int,default=180)
    p.add_argument("--sleep-between-requests",type=float,default=.5)
    p.add_argument("--temperature",type=float,default=0.0)
    p.add_argument("--synthesis-packet-size",type=int,default=30)
    p.add_argument("--synthesis-max-context-chars",type=int,default=24000)
    p.add_argument("--synthesis-output-tokens",type=int,default=5000)
    p.add_argument("--overwrite-synthesis",action="store_true")
    return p

def resolve(a):
    if not a.docs:
        return sorted(a.corpus.glob("*.pdf")) if a.corpus else []
    if not a.corpus: die("--corpus is required with --docs")
    ps=[a.corpus/x for x in a.docs]
    miss=[str(x) for x in ps if not x.exists()]
    if miss: die("Missing PDF(s):\n  "+"\\n  ".join(miss))
    return ps

def extract_pdf(p,max_pages=None):
    if pymupdf is None: die("Install PyMuPDF: pip install pymupdf")
    d=pymupdf.open(p); digest=sha256(p); rows=[]
    n=len(d) if max_pages is None else min(len(d),max_pages)
    for i in range(n):
        text=(d.load_page(i).get_text("text") or "").replace("\\x00","").strip()
        rows.append({
          "page_id":f"{stem(p.name)}:p{i+1:04d}",
          "document":p.name,"sha256":digest,"page":i+1,
          "text":text,"char_count":len(text)})
    d.close(); return digest,rows

def extraction_stage(a,paths,out):
    manifest={"schema_version":"star-docgen-manifest-v0.2","generator_version":VERSION,
              "created_utc":now(),"documents":[]}
    pages=[]
    for p in paths:
        digest,rows=extract_pdf(p,a.max_pages)
        print(f"Extracted {p.name}: {len(rows)} pages SHA256={digest}")
        pages += rows
        manifest["documents"].append({
          "filename":p.name,"path":str(p.resolve()),"sha256":digest,
          "page_count":len(rows) if a.max_pages else None,
          "pages_selected":len(rows)})
    manifest["document_count"]=len(paths); manifest["total_pages_selected"]=len(pages)
    write_json(out/"corpus_manifest.json",manifest)
    q=out/"page_evidence.jsonl"; tmp=q.with_suffix(".tmp")
    with open(tmp,"w",encoding="utf-8") as f:
        for r in pages: f.write(json.dumps(r,ensure_ascii=False)+"\n")
    tmp.replace(q)
    return pages

def chunks(pages,size,overlap,maxchars):
    if size<=overlap or size<1: die("--chunk-pages must be > --overlap-pages >= 0")
    by={}
    for p in pages: by.setdefault((p["document"],p["sha256"]),[]).append(p)
    out=[]
    for (doc,digest),ps in by.items():
        ps.sort(key=lambda x:x["page"]); step=size-overlap
        for start in range(0,len(ps),step):
            sel=ps[start:start+size]
            if not sel: break
            text=[]; used=0
            for p in sel:
                h=f"\\n===== {doc} | PDF page {p['page']} | {p['page_id']} =====\\n"
                rem=maxchars-used-len(h)
                if rem<=0: break
                text.append(h+p["text"][:rem]); used+=len(text[-1])
            cid=f"{stem(doc)}:p{sel[0]['page']:04d}-p{sel[-1]['page']:04d}:{digest[:12]}"
            out.append({"chunk_id":cid,"document":doc,"sha256":digest,
                        "page_start":sel[0]["page"],"page_end":sel[-1]["page"],
                        "page_ids":[x["page_id"] for x in sel],
                        "text":"".join(text)})
    return out

SYSTEM=r"""
You are the S.T.A.R. Evidence Extraction Engine. You are NOT writing or
summarizing a paper. Extract ONLY information explicitly supported by the
supplied pages. Do not use outside knowledge. Do not guess datasets.
Do not turn hypotheses/theoretical constructions into empirical facts.
Return JSON only.

Allowed types:
claim, definition, equation, algorithm, code, code_description, dataset,
experiment, result, limitation, conclusion, reference.

For each item preserve source distinctions between hypothesis, reasoning,
proposed method, actual implementation, theorized result and actual result.
For datasets capture name/filename, path only if explicit, catalog/survey/
database, record count, variables, preprocessing, and dataset_status.
If no dataset is explicitly named, dataset_status MUST be
"not_explicitly_identified".
For code capture language, code/excerpt, purpose, inputs, transformations,
outputs, dependencies. For experiments capture purpose, procedure, failures
if explicitly reported, dataset, code, theorized results and actual results.
"""

def prompt(c):
    return f"""Extract evidence from this bounded page group only.

CHUNK_ID: {c['chunk_id']}
DOCUMENT: {c['document']}
SHA256: {c['sha256']}
PAGES: {c['page_start']}-{c['page_end']}

Return:
{{"chunk_id":"{c['chunk_id']}","items":[
{{"type":"one_allowed_type","statement":"...",
"page_start":{c['page_start']},"page_end":{c['page_end']},
"source_quote":"...","explicit":true,
"hypothesis_status":"hypothesis|theoretical_construction|empirical|not_applicable",
"ideological_construction":null,"reasoning":null,
"theorized_result":null,"actual_result":null,
"dataset":null,"code":null,
"relationships":{{"code_ids":[],"experiment_ids":[],"dataset_ids":[],"result_ids":[]}}}}
]}}

Do not invent values.

PAGE TEXT:
{c['text']}"""

def ollama(a,system,prompt,max_tokens):
    body=json.dumps({"model":a.model,"system":system,"prompt":prompt,"stream":False,
                     "options":{"temperature":a.temperature,"num_predict":max_tokens}}).encode()
    req=urllib.request.Request(a.ollama_url,data=body,
        headers={"Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(req,timeout=a.request_timeout) as r:
        return json.loads(r.read().decode()).get("response","")

def parse_json(s):
    s=re.sub(r"^```(?:json)?\\s*|\\s*```$","",s.strip(),flags=re.I)
    try: return json.loads(s)
    except json.JSONDecodeError: pass
    i=s.find("{")
    if i<0: raise ValueError("No JSON object in Ollama response")
    depth=0; quote=False; esc=False
    for j in range(i,len(s)):
        ch=s[j]
        if quote:
            if esc: esc=False
            elif ch=="\\": esc=True
            elif ch=='"': quote=False
        elif ch=='"': quote=True
        elif ch=="{": depth+=1
        elif ch=="}":
            depth-=1
            if depth==0: return json.loads(s[i:j+1])
    raise ValueError("Unbalanced JSON from Ollama")

def next_e(out):
    rows=read_jsonl(out/"evidence"/"all_evidence.jsonl"); n=0
    for r in rows:
        m=re.match(r"E-(\\d+)$",str(r.get("evidence_id","")))
        if m:n=max(n,int(m.group(1)))
    return n+1

def normalize(raw,c,start):
    items=raw.get("items",[]) if isinstance(raw,dict) else []
    out=[]
    for i,x in enumerate(items):
        if not isinstance(x,dict) or x.get("type") not in TYPES: continue
        ps=max(c["page_start"],min(int(x.get("page_start",c["page_start"])),c["page_end"]))
        pe=max(ps,min(int(x.get("page_end",ps)),c["page_end"]))
        explicit=x.get("explicit",True)
        if isinstance(explicit,str): explicit=explicit.lower() in ("true","yes","explicit")
        r=dict(x); r.update({"evidence_id":f"E-{start+i:06d}","type":x["type"],
          "document":c["document"],"sha256":c["sha256"],"chunk_id":c["chunk_id"],
          "page_start":ps,"page_end":pe,"explicit":bool(explicit),
          "provenance":{"document":c["document"],"sha256":c["sha256"],
                        "page_start":ps,"page_end":pe,"chunk_id":c["chunk_id"]},
          "extracted_utc":now()})
        if r["type"]=="code": r["code_id"]=f"C-{start+i:06d}"
        if r["type"]=="dataset":
            ds=r.get("dataset") if isinstance(r.get("dataset"),dict) else {}
            if not ds.get("name"): ds["dataset_status"]="not_explicitly_identified"
            r["dataset"]=ds; r["dataset_id"]=f"DATA-{start+i:06d}"
        if r["type"]=="experiment":
            r["experiment_id"]=f"EXP-{start+i:06d}"
            ds=r.get("dataset")
            if not ds: r["dataset_status"]="not_explicitly_identified"
            elif isinstance(ds,str): r["dataset"]={"name":ds,"dataset_status":"explicit_name_only"}
        if r["type"]=="result": r["result_id"]=f"R-{start+i:06d}"
        out.append(r)
    return out

def state(out,name):
    p=out/"state"/name; p.parent.mkdir(parents=True,exist_ok=True); return p

def analyze(a,out):
    pages=read_jsonl(out/"page_evidence.jsonl")
    if not pages: die("Run extraction first.")
    cs=chunks(pages,a.chunk_pages,a.overlap_pages,a.max_context_chars)
    write_json(out/"chunk_manifest.json",{"generator_version":VERSION,"chunk_count":len(cs),
      "chunk_pages":a.chunk_pages,"overlap_pages":a.overlap_pages,
      "chunks":[{k:v for k,v in c.items() if k!="text"} for c in cs]})
    done={x.get("chunk_id") for x in read_jsonl(state(out,"completed.jsonl"))}
    failed={x.get("chunk_id") for x in read_jsonl(state(out,"failed.jsonl"))}
    target=[c for c in cs if (c["chunk_id"] in failed if a.retry_failed else c["chunk_id"] not in done)]
    if not target: print("No chunks require processing."); return
    e=next_e(out)
    for i,c in enumerate(target,1):
        print(f"[{i}/{len(target)}] {c['chunk_id']}")
        try:
            raw=ollama(a,SYSTEM,prompt(c),a.max_output_tokens)
            items=normalize(parse_json(raw),c,e); e+=len(items)
            allp=out/"evidence"/"all_evidence.jsonl"; allp.parent.mkdir(parents=True,exist_ok=True)
            for r in items:
                append_jsonl(allp,r); append_jsonl(out/"evidence"/FILES[r["type"]],r)
            append_jsonl(state(out,"completed.jsonl"),{"chunk_id":c["chunk_id"],
                "completed_utc":now(),"items":len(items)})
            append_jsonl(state(out,"ollama_requests.jsonl"),{"chunk_id":c["chunk_id"],
                "status":"completed","utc":now()})
            print(f"  evidence={len(items)}")
        except Exception as ex:
            err=f"{type(ex).__name__}: {ex}"
            print(f"  FAILED: {err}",file=sys.stderr)
            append_jsonl(state(out,"failed.jsonl"),{"chunk_id":c["chunk_id"],
                "failed_utc":now(),"error":err})
            append_jsonl(state(out,"ollama_requests.jsonl"),{"chunk_id":c["chunk_id"],
                "status":"failed","utc":now(),"error":err})
        if a.sleep_between_requests: time.sleep(a.sleep_between_requests)

SYNTH=r"""
You are the S.T.A.R. Scientific Manuscript Compiler. Write ONLY from the
supplied evidence ledger. Never invent facts, data, code, numbers, statistics,
citations, causality, or experimental success. Every substantive scientific
statement must carry evidence IDs like [E-000123; E-000124]. If support is
absent, write [UNSUPPORTED]. Do not silently reconcile contradictions.
Preserve distinctions between hypothesis, theoretical construction, proposed
method, actual implementation, theorized result, actual recorded result, and
limitation. If a dataset is not explicitly named, say so; never guess.
"""

def synth_section(a,out,section,ev):
    rows=[x for x in ev if x.get("type") in SECTIONS[section]]
    rows.sort(key=lambda x:(x.get("document",""),int(x.get("page_start",0)),x["evidence_id"]))
    packets=[rows[i:i+a.synthesis_packet_size] for i in range(0,len(rows),a.synthesis_packet_size)]
    if not packets: return f"# {section.title()}\\n\\n[UNSUPPORTED] No supporting evidence.\\n"
    drafts=[]
    for n,p in enumerate(packets,1):
        txt="\\n".join(json.dumps(x,ensure_ascii=False) for x in p)
        txt=txt[:a.synthesis_max_context_chars]
        pr=f"""Write a detailed {section} section from this evidence packet.
Cite every substantive statement with evidence IDs. Do not invent anything.
Preserve dataset/code/experiment/result relationships and [UNSUPPORTED].

EVIDENCE:
{txt}"""
        try: d=ollama(a,SYNTH,pr,a.synthesis_output_tokens)
        except Exception as ex: d=f"[UNSUPPORTED] Synthesis failure: {ex}"
        drafts.append(d.strip())
        if a.sleep_between_requests: time.sleep(a.sleep_between_requests)
    combined="\\n\\n".join(drafts)[:a.synthesis_max_context_chars]
    try:
        final=ollama(a,SYNTH,f"""Consolidate these bounded {section} packets.
Do not add facts. Retain evidence IDs and [UNSUPPORTED].

{combined}""",a.synthesis_output_tokens)
    except Exception: final=combined
    return f"# {section.title()}\\n\\n{final.strip()}\\n"

def provenance(out,manifest,ev):
    L=["# APPENDIX P — PROVENANCE","","## P.1 Corpus","",
       f"- Generator: v{VERSION}",f"- Documents: {manifest.get('document_count',0)}",
       f"- Pages: {manifest.get('total_pages_selected',0)}","","## P.2 Document hashes","",
       "| Document | SHA-256 | Pages |","|---|---|---:|"]
    for d in manifest.get("documents",[]):
        L.append(f"| `{d['filename']}` | `{d['sha256']}` | {d['pages_selected']} |")
    L += ["","## P.3 Evidence extraction methodology","",
      "PDFs are extracted page-by-page. Ollama receives bounded page windows only. "
      "Every evidence item retains PDF SHA-256, page range, chunk ID and evidence ID.",
      "","## P.4 Dataset provenance",""]
    ds=[x for x in ev if x.get("type")=="dataset"]
    if not ds: L.append("- No explicit dataset evidence was extracted.")
    for x in ds:
        d=x.get("dataset") if isinstance(x.get("dataset"),dict) else {}
        L.append(f"- `{x.get('dataset_id',x['evidence_id'])}`: "
                 f"{d.get('name','not explicitly identified')}; "
                 f"status=`{d.get('dataset_status','not_explicitly_identified')}`; "
                 f"{x['document']} pp.{x['page_start']}-{x['page_end']}; `{x['evidence_id']}`.")
    L += ["","## P.5 Code provenance",""]
    for x in ev:
        if x.get("type")=="code":
            L.append(f"- `{x.get('code_id',x['evidence_id'])}`: {x.get('statement','')} "
                     f"({x['document']} pp.{x['page_start']}-{x['page_end']}; `{x['evidence_id']}`).")
    L += ["","## P.6 Experiment provenance",""]
    for x in ev:
        if x.get("type")=="experiment":
            d=x.get("dataset")
            name=d.get("name") if isinstance(d,dict) else d
            L.append(f"- `{x.get('experiment_id',x['evidence_id'])}`: {x.get('statement','')}; "
                     f"dataset=`{name or 'not explicitly identified'}`; "
                     f"{x['document']} pp.{x['page_start']}-{x['page_end']}; `{x['evidence_id']}`.")
    L += ["","## P.7 Result provenance",""]
    for x in ev:
        if x.get("type")=="result":
            L.append(f"- `{x.get('result_id',x['evidence_id'])}`: {x.get('statement','')} "
                     f"({x['document']} pp.{x['page_start']}-{x['page_end']}; `{x['evidence_id']}`).")
    L += ["","## P.8 Cross-document dependencies","",
      "Relationships are preserved through evidence IDs, document hashes, pages and "
      "explicit source relationships. Similar filenames are not treated as identical datasets.",
      "","## P.9 Unsupported/ambiguous claims","",
      "The synthesis compiler marks unsupported substantive material as [UNSUPPORTED]. "
      "Unknown datasets remain not_explicitly_identified.","",
      "## P.10 Reproducibility notes","",
      "- Fixed PDF bytes are identified by SHA-256.",
      "- Chunk processing is resumable through state/completed.jsonl.",
      "- Failures are recorded in state/failed.jsonl.",
      "- Ollama requests are recorded in state/ollama_requests.jsonl.",
      "- Synthesis uses the evidence ledger, not the raw corpus.","",
      "## P.11 Evidence index","","| Evidence ID | Type | Document | Pages |",
      "|---|---|---|---:|"]
    for x in ev: L.append(f"| `{x['evidence_id']}` | `{x['type']}` | `{x['document']}` | {x['page_start']}-{x['page_end']} |")
    return "\\n".join(L)+"\\n"

def synthesize(a,out):
    ev=read_jsonl(out/"evidence"/"all_evidence.jsonl")
    if not ev: die("No evidence ledger. Run --analyze first.")
    m=json.loads((out/"corpus_manifest.json").read_text()) if (out/"corpus_manifest.json").exists() else {}
    sdir=out/"synthesis"; mdir=out/"manuscript"; sdir.mkdir(parents=True,exist_ok=True); mdir.mkdir(parents=True,exist_ok=True)
    sections={}
    for sec in ("theory","methods","experiments","results","discussion"):
        p=sdir/f"{sec}.md"
        if p.exists() and not a.overwrite_synthesis: sections[sec]=p.read_text()
        else:
            sections[sec]=synth_section(a,out,sec,ev); p.write_text(sections[sec],encoding="utf-8")
    man="# S.T.A.R. Scientific Manuscript\\n\\n"+f"Generated by v{VERSION}.\\n\\n"
    man+="> Substantive claims are required to carry evidence IDs; unsupported material is marked `[UNSUPPORTED]`.\\n\\n"
    man+="\\n\\n".join(sections[x] for x in ("theory","methods","experiments","results","discussion"))
    (mdir/"STAR_Scientific_Manuscript.md").write_text(man,encoding="utf-8")
    (mdir/"STAR_Provenance_Appendix.md").write_text(provenance(out,m,ev),encoding="utf-8")
    print("Wrote manuscript/STAR_Scientific_Manuscript.md")
    print("Wrote manuscript/STAR_Provenance_Appendix.md")

def main():
    a=parser().parse_args(); out=a.output.expanduser().resolve()
    for d in ("evidence","chunks","state","synthesis","manuscript"): (out/d).mkdir(parents=True,exist_ok=True)
    paths=resolve(a)
    if a.extract_only:
        if not paths: die("--extract-only requires --docs or --corpus")
        extraction_stage(a,paths,out)
    elif a.analyze:
        if not paths: die("--analyze requires --docs or --corpus")
        extraction_stage(a,paths,out); analyze(a,out)
    elif a.resume:
        if not (out/"page_evidence.jsonl").exists():
            if not paths: die("--resume needs existing page_evidence.jsonl or --corpus/--docs")
            extraction_stage(a,paths,out)
        analyze(a,out)
    elif a.retry_failed:
        if not (out/"page_evidence.jsonl").exists():
            if not paths: die("--retry-failed needs existing page_evidence.jsonl or --corpus/--docs")
            extraction_stage(a,paths,out)
        a.retry_failed=True; analyze(a,out)
    elif a.synthesize: synthesize(a,out)
    else: die("Choose --extract-only, --analyze, --resume, --retry-failed, or --synthesize.")

if __name__=="__main__": main()
