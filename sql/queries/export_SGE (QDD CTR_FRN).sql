WITH frn AS (
    SELECT DISTINCT ctr.CTR_T_NUM CONTRAT, acm.ACM_T_LIB FRN , acta.ACT_C_EIC EIC
    FROM CONTRAT.ASS_CTR_TAM_ACM acta
    JOIN CONTRAT.ACTEUR_MARCHE acm ON acm.ACM_ID = acta.ACM_ID
    JOIN CONTRAT.TYPE_ACTEUR tam ON tam.TAM_ID = acta.TAM_ID
    JOIN CONTRAT.CONTRAT ctr ON ctr.CTR_ID = acta.CTR_ID
    WHERE 1=1
    AND tam.TAM_C_CODE LIKE 'F%'
)

SELECT prm.PRM_ID as POINT, frn.EIC
FROM SGEL_PRM_SCH.T_PRM prm
	JOIN SGEL_PRM_SCH.T_SITUATION_CONTRACTUELLE situ ON prm.SCN_ID = situ.SCN_ID
	JOIN frn frn ON situ.SCN_CF_NUMERO_CONTRAT = frn.CONTRAT
WHERE 1=1
	AND situ.SCN_APP_APPLICATION_CODE = 'GINKO'
	AND situ.SCN_SEGMENT ='C5'
	AND prm.PRM_SC_ETAT_CONTRACTUEL_CODE = 'SERVC'
	AND prm.PRM_DG_APP_INSTANCE_SI = '@@RG_INSTANCE_CODE@@'
	--AND prm.PRM_ID IN ('22234876949527', '22565412341065', '22452677208285', '21178002857066', '22118813260640', '21247177850967', '21241823422616', '21230680057978', '21573371796674', '22579305248513')
	--AND prm.PRM_ID LIKE '211%'