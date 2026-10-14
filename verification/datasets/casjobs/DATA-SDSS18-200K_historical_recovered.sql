-- EXP-DATA-A01 / DATA-SDSS18-200K historical CasJobs reconstruction
-- Exact terminal query recovered from the 2026-10-08 CasJobs SQL history,
-- normalized only for whitespace and terminated with a semicolon.
--
-- IMPORTANT: this historical query has NO ORDER BY. A fresh rerun cannot prove
-- byte-identical membership of the original 200,000-row export. Do not use a
-- rerun mismatch as evidence that the preserved historical CSV is corrupted,
-- and do not use a rerun match to promote scientific evidence automatically.

SELECT TOP 200000
    p.objid,
    p.ra,
    p.dec,
    p.u,
    p.g,
    p.r,
    p.i,
    p.z,
    p.run,
    p.rerun,
    p.camcol,
    p.field,
    s.specobjid,
    s.class,
    s.z AS redshift,
    s.plate,
    s.mjd,
    s.fiberid
INTO mydb.MyTable
FROM PhotoObj AS p
JOIN SpecObj AS s
    ON s.bestobjid = p.objid
WHERE
    p.u BETWEEN 0 AND 19.6
    AND g BETWEEN 0 AND 20;
