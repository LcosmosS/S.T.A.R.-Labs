-- DATA-SDSS18-200K row-membership backcheck
--
-- PRECONDITION:
-- Upload a two-column table named mydb.STAR_SDSS18_200K_IDS containing the
-- frozen historical sample's objid and specobjid values, one pair per row.
--
-- This check can establish whether every frozen pair still resolves in the
-- DR18 PhotoObj/SpecObj relation and satisfies the recovered magnitude
-- predicates. It CANNOT recover the original unordered TOP 200000 selection
-- decision or prove the original job/export checksum.

SELECT
    COUNT(*) AS uploaded_rows,
    SUM(CASE WHEN p.objid IS NULL THEN 1 ELSE 0 END) AS missing_photoobj_rows,
    SUM(CASE WHEN s.specobjid IS NULL THEN 1 ELSE 0 END) AS missing_specobj_rows,
    SUM(
        CASE
            WHEN p.objid IS NOT NULL
             AND s.specobjid IS NOT NULL
             AND NOT (
                 p.u BETWEEN 0 AND 19.6
                 AND p.g BETWEEN 0 AND 20
             )
            THEN 1 ELSE 0
        END
    ) AS predicate_violation_rows
FROM mydb.STAR_SDSS18_200K_IDS AS h
LEFT JOIN PhotoObj AS p
    ON p.objid = h.objid
LEFT JOIN SpecObj AS s
    ON s.specobjid = h.specobjid
   AND s.bestobjid = p.objid;

SELECT
    h.objid AS uploaded_objid,
    h.specobjid AS uploaded_specobjid,
    p.objid AS resolved_objid,
    s.specobjid AS resolved_specobjid,
    p.u,
    p.g,
    s.class,
    s.z AS redshift
FROM mydb.STAR_SDSS18_200K_IDS AS h
LEFT JOIN PhotoObj AS p
    ON p.objid = h.objid
LEFT JOIN SpecObj AS s
    ON s.specobjid = h.specobjid
   AND s.bestobjid = p.objid
WHERE
    p.objid IS NULL
    OR s.specobjid IS NULL
    OR NOT (
        p.u BETWEEN 0 AND 19.6
        AND p.g BETWEEN 0 AND 20
    );
