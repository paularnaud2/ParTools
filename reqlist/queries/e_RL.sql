SELECT * FROM(		
SELECT seg.PRM_ID POINT		
, srv.SERVICE_ID SRV_ADAM, srv.SERVICE_TYPE, srv.ETAT_CODE		
, TO_CHAR(srv.DATE_DEBUT, 'DD/MM/YYYY') DATE_DEBUT		
, TO_CHAR(srv.DATE_FIN, 'DD/MM/YYYY') DATE_FIN		
, TO_CHAR(srv.DATE_MODIFICATION, 'DD/MM/YYYY') DATE_MODIF		
, srv.MOTIF_FIN_LIBELLE, srv.PERIODICITE_TRANSMISSION PER_TR		
, mes.TYPE_CODE as TYPE_MES, mes.PAS as PAS_MES		
, CASE  WHEN ben.TYPE = 'PERSONNE' THEN 'Client'		
		WHEN ben.TYPE = 'FINALITE' THEN 'Interne'
		WHEN ben.TYPE = 'CONTRAT' AND (ben.code LIKE 'GRD-F%' or ben.code = 'PROTOC-501') THEN 'Fournisseur'
		WHEN ben.TYPE = 'CONTRAT' AND NOT (ben.code LIKE 'GRD-F%' or ben.code = 'PROTOC-501') THEN 'Tiers'
		ELSE 'Indéterminé'
		END "TYPE_DEM"
, CASE  WHEN ben.TYPE = 'FINALITE' THEN ben.CODE		
		WHEN ben.TYPE = 'CONTRAT' THEN ben.LIBELLE
		END "DEM"
, DENSE_RANK() OVER (PARTITION BY seg.PRM_ID ORDER BY srv.DATE_FIN DESC) RANG		
FROM ADA_SCH.SERVICE_SOUSCRIT srv		
LEFT JOIN ADA_SCH.BENEFICIAIRE ben ON srv.BENEFICIAIRE_ID = ben.ID		
LEFT JOIN ADA_SCH.PRM_SEGMENT seg ON srv.PRM_SEGMENT_ID = seg.ID		
LEFT JOIN ADA_SCH.MESURE mes ON srv.MESURE_ID = mes.ID		
WHERE 1=1		
AND seg.SEGMENT = 'C5'		
AND srv.SERVICE_TYPE = 'TRANSREC'		
AND mes.TYPE_CODE = 'CDC'		
AND seg.PRM_ID IN @@IN@@		
 -- AND seg.PRM_ID = '01100289413189'		
)		
WHERE RANG = 1