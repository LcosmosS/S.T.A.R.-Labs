#!/usr/bin/env node
/** Exclude unadmitted static sky files from deploys, even if staged in Git.
 * Run only AFTER sky:check; this is a deployment filter, not a review authority.
 */
import { readFile, readdir, unlink, stat } from "node:fs/promises";
import { dirname, join, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT=resolve(dirname(fileURLToPath(import.meta.url)),"..");
const PREFIX="web_tool/public/sky/";

export async function filterSkyAssets(publicSkyDir, manifest) {
  if (!manifest || manifest.schemaVersion!=="star-sky-overlay-releases-v1" || !Array.isArray(manifest.sources))
    throw new Error("sky admission manifest unavailable; refuse deployment");
  const approved=new Set();
  for(const entry of manifest.sources) {
    const path=entry?.coordinatePath;
    if(typeof path!=="string"||!path.startsWith(PREFIX))throw new Error("unsafe approved sky coordinate path");
    const relative=path.slice(PREFIX.length);
    if(!relative || relative.includes("\\") || relative.split("/").some(p=>!p||p==="."||p===".."))
      throw new Error("unsafe approved sky coordinate filename");
    approved.add(relative);
  }
  const dir=resolve(publicSkyDir);
  let removed=0;
  async function inspect(folder) {
    for(const e of await readdir(folder,{withFileTypes:true})) {
      const full=join(folder,e.name), relative=full.slice(dir.length+1).split(sep).join("/");
      if(e.isDirectory())await inspect(full);
      else if(e.isFile()) {
        if(!approved.has(relative)){await unlink(full);removed++;}
      } else throw new Error("unexpected symlink/device in published sky directory");
    }
  }
  try{await inspect(dir);}catch(e){if(e.code!=="ENOENT")throw e;}
  for(const relative of approved) {
    const full=resolve(dir,relative);
    if(!full.startsWith(dir+sep) || !(await stat(full)).isFile())
      throw new Error("admitted coordinate bytes missing after deploy filtering: "+relative);
  }
  return {approved:approved.size,removed};
}
async function main(){
  const manifest=JSON.parse(await readFile(join(ROOT,"content/sky-overlay-releases.v1.json"),"utf8"));
  const r=await filterSkyAssets(join(ROOT,"public/sky"),manifest);
  console.log("Sky deploy filter:",r.approved,"approved assets;",r.removed,"unadmitted removed");
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))
  main().catch(e=>{console.error(e);process.exitCode=1;});
