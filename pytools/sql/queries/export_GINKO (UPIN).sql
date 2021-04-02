SELECT pds.REFERENCE as PDS
, DECODE(pds.ETAT,
        '1', 'ne peut être mis en service',
        '3', 'hors service',
        '4', 'en service',
        '5', 'supprimé',
        '12', 'non raccordable',
        '13', 'raccordable',
        'inconnu') as ETAT
, DECODE(pds.SOUSETAT,
        '1', 'actif',
        '2', 'libre service',
        '3', 'depose',
        '4', 'debranche',
        '5', 'debranche au branchement',
        '6', 'sans objet',
        '7', 'debranche au CCPI',
        '8', 'organe compteur ouvert') as SOUSETAT
, DECODE(ctr.EXTRAITSERVICESSOUSCRIT,
        'CUSDT', 'CUST',	
        'MUADT', 'MUDT',
        'MUADT2', 'MUDT',
        'LUSDT', 'LU',
        'CUADT4', 'CU4',
        'MUADT4', 'MU4')as FTA
, srv.USAGE as CTX
, DECODE(ctr.STATUTEXTRAIT,
        '0', 'en cours de souscription',
        '1', 'actif',
        '2', 'en cours de modification',
        '3', 'en cours de cessation',
        '4', 'cessé',
        '5', 'cessation partielle',
        '8', 'annulé',
        'inconnu') as STATUT
, pds.DATECREATION
, srv.DATEEFFET
FROM GAHFLD.TESPACEDELIVRAISON edl
   JOIN GAHFLD.TPOINTDESERVICE pds ON edl.ID = pds.ESPACEDELIVRAISON_ID
   JOIN GAHFLD.CONTRAT_ESPACESDELIVRAISON ce ON edl.ID = ce.DEST
   JOIN GAHFLD.TCONTRAT ctr ON ce.SOURCE = ctr.ID
   LEFT JOIN GAHFLD.TSERVICESOUSCRIT srv ON ctr.ID = srv.CONTRAT_ID
WHERE 1=1
   AND ctr.DATEFIN IS NULL
   AND srv.DATEFIN IS NULL
   AND srv.ROLE = 'com.hermes.crm.contrat.businessobject.ServiceSouscritAcheminementElecBTInf36'
   AND ctr.EXTRAITSERVICESSOUSCRIT = 'LUSDT'
   AND pds.ETAT = '4'
   AND pds.SOUSETAT = '1'
   AND srv.USAGE = 'PRONUIPLA'
   AND srv.DATEEFFET < pds.DATECREATION
   --AND pds.REFERENCE = '01627641014608'