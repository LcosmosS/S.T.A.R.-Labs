/** Discovery metadata from the current README, separate from scientific gates. */
export function publicationsFromReadme(readme) {
  const normalized = `\n${readme.replace(/\r\n/g, "\n")}`;
  return [
    ["M1-INH-E1b", "M1-INH-E1b — Pre-review package v0.1"],
    ["EXP-MAP-A01", "EXP-MAP-A01 — Preregistration, activation and reproducibility package v0.1"],
    ["EXP-MAP-A03", "EXP-MAP-A03 — Published pre-execution verification archive v0.1"],
  ].map(([id, title]) => {
    const sections = normalized.split(`\n### ${title}\n`);
    if (sections.length > 2) throw new Error(`Ambiguous README publication heading: ${id}`);
    const section = sections[1] === undefined ? undefined : `\n${sections[1]}`.split(/\n---|\n#{1,3} /)[0];
    const doi = section?.match(/https:\/\/doi\.org\/10\.5281\/zenodo\.\d+/)?.[0];
    const release = section?.match(/https:\/\/github\.com\/LcosmosS\/S\.T\.A\.R\.-Labs\/releases\/tag\/[^)\s]+/)?.[0];
    const status = section?.match(/\*\*Scientific status:\*\* ([^\n]+)/)?.[1];
    if (!doi || !release || !status) throw new Error(`Missing current README publication metadata: ${id}`);
    const reviewLinks = [...new Set(section.match(/https:\/\/github\.com\/LcosmosS\/S\.T\.A\.R\.-Labs\/pull\/\d+/g) ?? [])];
    return { id, title, doi, release, status: status.replace(/\*\*/g, ""), reviewLinks, sourcePath: "README.md" };
  });
}
