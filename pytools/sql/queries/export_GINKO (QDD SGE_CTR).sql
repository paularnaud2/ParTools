WITH CTR_RANK as
(
    SELECT pds.REFERENCE as POINT
    , DENSE_RANK() OVER (PARTITION BY pds.REFERENCE ORDER BY ctr.DATECREATION DESC) as RANG
    , DECODE(ctr.STATUTEXTRAIT,
        '0', 'en cours de souscription',
        '1', 'actif',
        '2', 'en cours de modification',
        '3', 'en cours de cessation',
        '4', 'cessé',
        '5', 'cessation partielle',
        '8', 'annulé',
        'inconnu') as STATUT
    FROM GAHFLD.TESPACEDELIVRAISON edl
    JOIN GAHFLD.TPOINTDESERVICE pds ON edl.ID = pds.ESPACEDELIVRAISON_ID
    LEFT JOIN GAHFLD.CONTRAT_ESPACESDELIVRAISON ce ON edl.ID = ce.DEST
    LEFT JOIN GAHFLD.TCONTRAT ctr ON ce.SOURCE = ctr.ID
    WHERE 1=1
    AND pds.DATESUPPRESSION IS NULL
    AND ctr.STATUTEXTRAIT IN ('1', '2', '3', '4')
    --AND pds.REFERENCE LIKE '211%'
)

, CTR_RANK1 as
(
    SELECT POINT, STATUT FROM CTR_RANK
    WHERE RANG = 1
)

, PDS as
(
SELECT pds.REFERENCE as POINT
FROM GAHFLD.TPOINTDESERVICE pds
WHERE 1=1
AND pds.ETAT <> '5'
AND pds.DATESUPPRESSION IS NULL
AND pds.REFERENCE NOT LIKE '000%'
--AND pds.REFERENCE LIKE '211%'
--AND pds.REFERENCE = '21193777062650'
)

SELECT pds.POINT
, CASE WHEN STATUT = ('cessé') OR STATUT IS NULL THEN '0'
       ELSE '1'
  END as ETAT
FROM PDS pds
LEFT JOIN CTR_RANK1 c ON pds.POINT = c.POINT