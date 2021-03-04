--Requete EDF Commerce Hebdo et quotidienne à partir du 14 décembre
SELECT * FROM AFF
WHERE PRM LIKE '@@RG_PRM_2@@%'
AND ROWNUM < 150