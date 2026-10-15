-- DATA-SDSS18-200K historical-query rerun recipe
--
-- The archival DATA-SDSS18-200K_historical_recovered.sql remains the exact
-- normalized recovered query, including its original INTO mydb.MyTable.
--
-- For an independent rerun, submit THIS recipe in the DR18 CasJobs context
-- using the Submit button and provide a UNIQUE output name in the CasJobs
-- "Table" field. Omitting a fixed INTO destination avoids MyDB name collisions
-- without requiring a cross-context DROP TABLE.
--
-- This recipe preserves the recovered SELECT/JOIN/predicates and still has NO
-- ORDER BY, so a fresh result cannot prove the exact original TOP 200000
-- membership decision.

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
FROM PhotoObj AS p
JOIN SpecObj AS s
    ON s.bestobjid = p.objid
WHERE
    p.u BETWEEN 0 AND 19.6
    AND g BETWEEN 0 AND 20;
