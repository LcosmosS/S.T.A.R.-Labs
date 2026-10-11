#!/usr/bin/env node
/** Stage only approved static sky files for Vite builds.
 * Never delete tracked files in web_tool/public; copy other public assets
 * unchanged. Sky-release approval remains governed by sky:check and a
 * separately accountable human review.
 */
import { copyFile, mkdir, readFile, readdir, rm } from "node:fs/promises";
import { dirname, join, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT=resolve(dirname(fileURLToPath(import.meta.url)),"..");
const PREFIX="web_tool/public/sky/";

/** Build a disposable public-assets tree, excluding every unadmitted sky file. */
export async function filterSkyAssets(publicDir, stagingDir, manifest) {
  if(!manifest||manifest.schemaVersion!=="star-sky-overlay-releases-v1"||
     !Array.isArray(manifest.sources))
    throw new Error("sky admission manifest unavailable; refuse deployment");
  const src=resolve(publicDir), dest=resolve(stagingDir);
  if(dest===src||dest.startsWith(src+sep)||src.startsWith(dest+sep))
    throw new Error("staging directory must be outside the tracked public source");
  const approved=new Set();
  for(const item of manifest.sources) {
    const path=item?.coordinatePath;
    if(typeof path!=="string"||!path.startsWith(PREFIX))
      throw new Error("unsafe approved sky coordinate path");
    const name=path.slice(PREFIX.length);
    if(!name||name.includes("\\")||name.split("/").some(
      s=>!s||s==="."||s===".."||!/^[a-zA-Z0-9_.-]+$/.test(s)))
      throw new Error("unsafe approved sky coordinate filename");
    if(approved.has(name))throw new Error("duplicate approved sky filename");
    approved.add(name);
  }
  let copied=0,excluded=0;
  const admitted=new Set();
  // The generated build input, NOT the checked-in source, is disposable.
  await rm(dest,{recursive:true,force:true});
  await mkdir(dest,{recursive:true});
  async function copyTree(folder) {
    for(const entry of await readdir(folder,{withFileTypes:true})) {
      const full=join(folder,entry.name);
      const rel=relative(src,full).split(sep).join("/");
      const output=join(dest,rel);
      if(entry.isDirectory()) {
        await mkdir(output,{recursive:true});
        await copyTree(full);
      }else if(entry.isFile()) {
        if(rel.startsWith("sky/")) {
          const skyFile=rel.slice(4);
          if(!approved.has(skyFile)) {excluded++;continue}
          admitted.add(skyFile);
        }
        await mkdir(dirname(output),{recursive:true});
        await copyFile(full,output);
        copied++;
      } else throw new Error("unexpected symlink or device in public assets");
    }
  }
  await copyTree(src);
  for(const file of approved)
    if(!admitted.has(file))
      throw new Error("admitted coordinate bytes missing from tracked public source: "+file);
  return {approved:approved.size,excluded,copied};
}
async function main() {
  const manifest=JSON.parse(await readFile(join(ROOT,"content/sky-overlay-releases.v1.json"),"utf8"));
  const r=await filterSkyAssets(join(ROOT,"public"),join(ROOT,".sky-public-build"),manifest);
  console.log("Sky public build staged:",r.approved,"approved;",r.excluded,
              "excluded;",r.copied,"files copied. Tracked source untouched.");
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))
  main().catch(e=>{console.error(e);process.exitCode=1;});
