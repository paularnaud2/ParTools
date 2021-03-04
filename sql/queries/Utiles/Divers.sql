--Colones et tables
SELECT * FROM ALL_TAB_COLUMNS
WHERE 1=1
AND COLUMN_NAME LIKE '%ANNUL%'
AND OWNER LIKE '%IAP%'
--AND TABLE_NAME = 'T_SITUATION_CONTRACTUELLE';
ORDER BY 3

--Requete pour generer la commande de désactivation d'une contrainte pour une table donnée : 
select 'ALTER TABLE '||a.owner||'.'||a.table_name||' DISABLE CONSTRAINT '||a.constraint_name||';'
from all_constraints a, all_constraints b
where a.constraint_type = 'R'
and a.r_constraint_name = b.constraint_name
and a.r_owner = b.owner
and b.table_name = 'T_AFFAIRE'
and a.constraint_name = 'FK_T_PRESTATION_AFF_ID_S';

SELECT * FROM ALL_CONSTRAINTS WHERE CONSTRAINT_NAME = 'FK_T_SITUATION_CON_SCN_INTE'

--Sélection de tous les noms de colonnes pour un user donné.
SELECT * FROM ALL_TAB_COLUMNS WHERE OWNER = 'C5'
;

-----Check directories-------
SELECT * FROM ALL_DIRECTORIES;

----------Requêtes spéciales (à lancer avec le user SYSTEM)-------------------------------
SELECT * FROM DICTIONARY
WHERE TABLE_NAME LIKE 'DBA_T%'
;

--Table space------------------
SELECT * FROM DBA_TABLESPACES;

--Affiche la liste des acteurs de marché actifs avec un jeu de données qui peuvent être utiles
SELECT DISTINCT acm.ACM_T_LIB "Acteur de marché", acm.ACM_C_CODE "Code SGE de l'acteur de marché", acm.ACM_ID, acta.ACT_C_EIC "Code EIC de l'acteur de marché", ata.ATA_C_DISCO "Commercialisateur DISCO"
FROM CONTRAT.ASS_CTR_TAM_ACM acta
JOIN CONTRAT.ACTEUR_MARCHE acm ON acm.ACM_ID = acta.ACM_ID
JOIN CONTRAT.TYPE_ACTEUR tam ON tam.TAM_ID = acta.TAM_ID
JOIN CONTRAT.ASS_TAM_ACM ata ON ata.ACM_ID = acm.ACM_ID
WHERE    1=1
--AND ata.ATA_C_DISCO = '01'
AND tam.TAM_C_CODE = 'FOURNISSEUR'
AND tam.TAM_ID = ata.TAM_ID
ORDER BY ATA_C_DISCO
;

--Trouve des logins actifs par ACM_ID
SELECT DISTINCT uti.UTI_T_LOGIN FROM UTILISATEUR.UTILISATEUR uti
JOIN UTILISATEUR.ASS_PRF_UTI prf ON uti.UTI_ID = prf.UTI_ID
WHERE uti.ACM_ID = '27'
AND uti.UTI_B_ACTIF = 'O'
AND prf.APU_B_ACTIF = 'O'
ORDER BY uti.UTI_T_LOGIN ASC
;

--Liste prestas SGEL
SELECT DISTINCT NAT_C_TYPE as PRS, NAT_C_SOUS_TYPE as OPT
FROM SUIVI.DEMANDE dem
JOIN SUIVI.NATURE nat ON dem.DEM_K_NAT = nat.NAT_ID
WHERE DEM_B_IS_SGEL = 'O'
ORDER BY NAT_C_TYPE
;

--Codes retour DISCO
SELECT * FROM DISCO.CODE_RETOUR_DISCO_4_0 cr
JOIN DISCO.PROCESSUS_DISCO prc ON cr.PRD_ID = prc.PRD_ID
JOIN DISCO.MESSAGE_RETOUR_DISCO_4_0 mrd ON mrd.CRD_ID = cr.CRD_ID
JOIN DISCO.FAISABILITE fai ON fai.FAI_ID = mrd.FAI_ID
ORDER BY cr.CRD_C_CODE_DISCO
;

--Batchs SGEL
SELECT inst.JOB_NAME, batch.START_TIME, EXTRACT(SECOND FROM (batch.END_TIME - batch.START_TIME)) as DUREE_S
FROM SGEL_BATCH_SCH.BATCH_JOB_EXECUTION batch
JOIN SGEL_BATCH_SCH.BATCH_JOB_INSTANCE inst ON inst.JOB_INSTANCE_ID = batch.JOB_INSTANCE_ID
WHERE JOB_NAME LIKE '%C15%'
ORDER BY batch.START_TIME DESC
;

--Opération / services
SELECT  srv.C_SERVICE, op.C_OPERATION FROM TUBE.TUBE_OPERATION_SERVICE op
JOIN TUBE.TUBE_SERVICE srv ON op.ID_SERVICE = srv.ID_SERVICE
;

--Tracer demandes non recevables
SELECT *
FROM SGEL_ARCHIVAGE_SCH.T_TRACE_AUDIT_PAR_PRM trace
--JOIN SGEL_PRM_SCH.T_SITUATION_CONTRACTUELLE situ ON trace.TAP_ID_PRM = situ.SCN_APP_REF_POINT
WHERE 1=1
--AND situ.SCN_SITU_TYPE = 'C'
--AND situ.SCN_APP_APPLICATION_CODE = 'GINKO'
AND TAP_TYPE_TRACE = 'tracerDemandeNonRecevable'
AND trace.TAP_DATE_TRACE > '01/05/19'
AND trace.TAP_DATE_TRACE < '03/05/19'
--AND trace.TAP_ID_PRM = '23227785757066'
;

--Export csv
set heading off
set echo off
set feedback off
set pagesize 0
spool "C:\Users\A51575\Documents\CAPT\CHF.csv";
SELECT /*csv*/ a.pdm_id,
  a.AFF_T_DISCO,
echo off;

@"C:\Mes données\Fichiers\SQL\export.sql"

--Recherche d'une table ou d'une colonne
SELECT * FROM ALL_TAB_COLUMNS
WHERE 1=1
AND OWNER NOT LIKE '%SYS%'
AND TABLE_NAME NOT LIKE 'TMP_%'
--AND TABLE_NAME LIKE '%GROUP%'
AND COLUMN_NAME LIKE '%SEG%'
;

--Recherche de tables volumineuses
SELECT OWNER, TABLE_NAME, MAX(NUM_DISTINCT)
FROM ALL_TAB_COLUMNS
WHERE 1=1
AND OWNER NOT LIKE '%SYS%'
AND NUM_DISTINCT IS NOT NULL
GROUP BY OWNER, TABLE_NAME
ORDER BY 3 DESC
;