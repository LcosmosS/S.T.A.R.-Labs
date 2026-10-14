-- DATA-SDSS18-200K historical-query rerun wrapper
--
-- The archived DATA-SDSS18-200K_historical_recovered.sql remains an exact
-- normalized record of the recovered terminal query and is not modified for
-- rerunnability. This wrapper clears the historical MyDB destination and then
-- executes the same SELECT/JOIN/predicates. It still has NO ORDER BY, so a
-- fresh result is not expected to prove exact historical membership.

IF OBJECT_ID('mydb.MyTable', 'U') IS NOT NULL
    DROP TABLE mydb.MyTable;

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
