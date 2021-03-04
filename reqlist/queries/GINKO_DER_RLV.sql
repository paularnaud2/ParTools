WITH a AS (
SELECT /*+ PARALLEL(8) ORDERED */ DISTINCT pds.Reference PDS
	, CASE WHEN pds.Nature = 2 THEN 'Producteur en Totalité'
		  WHEN pds.ParticularitePDS = 1 THEN 'Producteur en Surplus'
		  WHEN pds.Nature = 1 THEN 'Consommation'
		  ELSE NULL END as TYPE_PDS
	, TO_CHAR(rel.DateReleve, 'DD/MM/YYYY') D
	, DECODE(rel.STATUTRELEVE,1,'valide', 2, 'invalide', 3, 'en cours de traitement', NULL, NULL, rel.STATUTRELEVE || '-INCONNU') STA
	, DECODE(rel.FactureGRD, 0, 'NON Facturée', 1, 'Facturée') AS FACT
	, DECODE(rel.TYPERELEVE, '1','récurrente', '21','de régularisation avec index', '22','de régularisation sans index', '3','sur événement') TYPE_RLV
	, DECODE(rel.NATURERELEVE, '1','réelle', '2','estimé suite à absence client', '3','estimé entre 2 relèves réelles', '4','absence à la relève', '5','estimé','6','evt réelle','41','avec idx réelle','42','avec idx estimée','51','sans idx réelle','52','sans idx estimée','7','absence relève','9','evt estimée') NAT 
	, DECODE(rel.AUTORELEVE,0,'NON',1,'OUI') AUTORELEVE
	, DENSE_RANK() OVER (PARTITION BY pds.ID ORDER BY pacm.DateDebut DESC NULLS LAST, rel.DateReleve DESC NULLS LAST, rel.STATUTRELEVE, rel.TYPERELEVE) RANG
	FROM gahfld.TPOINTDESERVICE pds
	INNER JOIN gahfld.TPACM pacm ON (pacm.PointDeService_ID = pds.ID)
	LEFT JOIN gahfld.TRELEVE rel ON (rel.Pacm_ID = pacm.ID)
	WHERE 1=1
	AND pds.ETATOBJET = '0'
	AND pds.ETAT <> '5'
	AND rel.STATUTRELEVE <> '2'
	AND rel.NATURERELEVE IN ('1', '6', '41')
	-- AND pds.Reference IN ('19425180866829')
	AND pds.Reference IN @@IN@@
)

SELECT a.PDS POINT, a.TYPE_PDS
, a. NAT NATURE_RLV, a.D DATE_DER_RLV, a.STA STATU_DER_RLV, a.FACT FACT_DER_RLV, a.TYPE_RLV TYPE_DER_RLV, a.AUTORELEVE AUTORLV_DER_RLV
--, b.D DATE_RLV_PREC, b.STA STATU_RLV_PREC, b.FACT FACT_RLV_PREC, b.TYPE_RLV TYPE_RLV_PREC, b.AUTORELEVE AUTORLV_RLV_PREC
FROM a
--JOIN a b ON a.PDS = b.PDS AND b.RANG = 2
WHERE a.RANG = 1
;