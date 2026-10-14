-- DATA-SDSS18-200K deterministic independent probe
--
-- This is NOT a reconstruction of the historical row membership. It applies
-- the recovered schema, join, and magnitude predicates to the current DR18
-- context with an explicit order so an independent reviewer can obtain a
-- stable comparison sample. The output must never replace the preserved
-- historical CSV or silently change DATA-SDSS18-200K provenance.

IF OBJECT_ID('mydb.STAR_SDSS18_200K_DETERMINISTIC_PROBE', 'U') IS NOT NULL
    DROP TABLE mydb.STAR_SDSS18_200K_DETERMINISTIC_PROBE;

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
INTO mydb.STAR_SDSS18_200K_DETERMINISTIC_PROBE
FROM PhotoObj AS p
JOIN SpecObj AS s
    ON s.bestobjid = p.objid
WHERE
    p.u BETWEEN 0 AND 19.6
    AND p.g BETWEEN 0 AND 20
ORDER BY
    p.objid ASC,
    s.specobjid ASC;
