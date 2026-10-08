#!/usr/bin/env node
import {readFile,writeFile} from "node:fs/promises";
import {resolve,dirname} from "node:path";
import {fileURLToPath} from "node:url";
const root=resolve(dirname(fileURLToPath(import.meta.url)),"../..");
const sourcePath="web_tool/content/research-content-v0.1.json";
const outPath="web_tool/src/lib/star/research-content-snapshot.json";
const okStatuses=new Set(["model_exploratory","derived_conditional","historical_unreplicated","archive_only"]);
const okKinds=new Set(["projection","equation","reduction","diagram","reported_result","notebook"]);
function validate(model) {
  if(model.schemaVersion!=="WEB-CONTENT-v0.1"||model.readOnly!==true||model.governingCharter!=="charter/STAR_Research_Charter_v0-2.pdf") throw Error("Governance mismatch");
  if(model.externalSource.committed!==false||!/^[a-f0-9]{64}$/.test(model.externalSource.sha256)) throw Error("Historical source identity mismatch");
  if(!Array.isArray(model.items)||model.items.length<6) throw Error("Incomplete research catalog");
  const seen=new Set();
  for(const item of model.items) {
    if(!/^WEB-[A-Z0-9-]+$/.test(item.id)||seen.has(item.id)) throw Error("Duplicate or invalid ID");
    seen.add(item.id);
    if(!okKinds.has(item.kind)||!okStatuses.has(item.status)||!["M","D"].includes(item.epistemic)) throw Error("Unsupported evidence status");
    if(item.epistemic==="D"&&item.status!=="derived_conditional") throw Error("Derived-status mismatch");
    if(item.kind==="reported_result"&&item.status!=="historical_unreplicated") throw Error("Unreplicated metric promotion");
    if(item.kind==="notebook"&&item.status!=="archive_only") throw Error("Executable notebook promotion");
    for(const field of ["title","summary","caveat","source"]) if(typeof item[field]!=="string"||!item[field].trim()) throw Error("Missing limitation or source");
    if(item.sourcePath&&(item.sourcePath.startsWith("/")||item.sourcePath.includes("..")||!/^[a-zA-Z0-9_./&-]+$/.test(item.sourcePath))) throw Error("Unsafe source path");
    if(item.kind==="diagram"&&(!Array.isArray(item.diagramSteps)||item.diagramSteps.length<3)) throw Error("Missing diagram steps");
  }
  return model;
}
const args=process.argv.slice(2);
if(args.length>1||(args.length===1&&args[0]!=="--check")) throw Error("Usage: sync-research-content.mjs [--check]");
const model=validate(JSON.parse(await readFile(resolve(root,sourcePath),"utf8")));
const result=JSON.stringify({schemaVersion:"WEB-SNAPSHOT-v0.1",readOnly:true,sourcePath,model},null,2)+"\n";
if(args.length){if(await readFile(resolve(root,outPath),"utf8")!==result)throw Error("Stale research snapshot");console.log("Research snapshot valid: "+model.items.length+" qualified entries");}
else{await writeFile(resolve(root,outPath),result);console.log("Research snapshot regenerated");}
