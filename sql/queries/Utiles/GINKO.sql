--Point, contrat
SELECT pds.REFERENCE as PDS
, CASE
	WHEN pds.Nature = 2 THEN 'Producteur en Totalité'
	WHEN pds.ParticularitePDS = 1 THEN 'Producteur en Surplus'
	WHEN pds.Nature = 1 THEN 'Consommation'
	ELSE NULL
	END AS TypePDS
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
, pds.COUPE
, DECODE(pds.RAISONCOUPURE,
		  '0', 'sécurité',
		  '1', 'non-paiement',
		  '3', 'absence relève',
		  '5', 'suspension contractuelle',
		  'inconnu') as RAISONCOUPURE
, SUBSTR(pds.PALIERTECHNIQUE, 4, 2) P_RAC
, pds.NBCADRANSCOMPTEUR
, pds.TECHNOLOGIETELERELEVE
, pds.ELIGIBILITEDEPLOIEMENTAMMMASSE
, pds.RELEVEACCESSIBLE
, pds.COMPTEURACCESSIBLE
, pds.NOMBREABSENCERELEVESUCCESSIVE
, pds.COMPTEURABSENCERELEVEMODIFIE
, pds.STATUTINFRASTRUCTUREAMM
, pds.AMMCOMMUNICANT
, pds.COMMUNICABILITEAMM
, pds.NIVEAUCOMMUNICABILITEAMM
, ctr.REFERENCE as REF_CTR, ctr.DATEEFFETEXTRAIT
, DECODE(ctr.EXTRAITSERVICESSOUSCRIT,
		  'CUSDT', 'CUST',	
		  'MUADT', 'MUDT',
		  'MUADT2', 'MUDT',
		  'LUSDT', 'LU',
		  'CUADT4', 'CU4',
		  'MUADT4', 'MU4')as FTA
, srv.USAGE as CAT_CLIENT_CTX
, DECODE(ctr.STATUTEXTRAIT,
		  '0', 'en cours de souscription',
		  '1', 'actif',
		  '2', 'en cours de modification',
		  '3', 'en cours de cessation',
		  '4', 'cessé',
		  '5', 'cessation partielle',
		  '8', 'annulé',
		  'inconnu') as STATUT
, REPLACE(srv.PUISSANCESOUSCRITE1_VALUE,'.',',') PS
, op.LIBELLE as OFFRE_PRODUIT, act.NOM as FOURNISSEUR
, cafo.REFERENCE as CALENDRIER
, dga.LIBELLE as DG_ACTIVE, dgp.LIBELLE as DG_PROGRAMMEE, dgf.LIBELLE as DG_FUTURE
, tmat.CONSTRUCTEUR
, mat.ROLE
, dgeo.COMMUNE_LIBELLE as COMMUNE
, prog_rlv.DATETHEORIQUERELEVE as DTR
FROM GAHFLD.TESPACEDELIVRAISON edl
	JOIN GAHFLD.TPOINTDESERVICE pds ON edl.ID = pds.ESPACEDELIVRAISON_ID
	JOIN GAHFLD.CONTRAT_ESPACESDELIVRAISON ce ON edl.ID = ce.DEST
	JOIN GAHFLD.TCONTRAT ctr ON ce.SOURCE = ctr.ID
	LEFT JOIN GAHFLD.TSERVICESOUSCRIT srv ON ctr.ID = srv.CONTRAT_ID
	LEFT JOIN GAHFLD.TROLE rol ON ctr.TITULAIRE_ID = rol.ID
	LEFT JOIN GAHFLD.TACTEUR act ON rol.ACTEUR_ID = act.ID
	LEFT JOIN GAHFLD.TOFFREPRODUIT op ON ctr.OFFREPRODUIT_ID = op.ID
	LEFT JOIN GAHFLD.TDECLINAISONGEOGRAPHIQUE dga ON pds.DECLINAISONGEOACTIVE_ID = dga.ID
	LEFT JOIN GAHFLD.TDECLINAISONGEOGRAPHIQUE dgf ON pds.DECLINAISONGEOFUTURE_ID = dgf.ID
	LEFT JOIN GAHFLD.TPACM pacm ON pds.ID = pacm.POINTDESERVICE_ID
	LEFT JOIN GAHFLD.TPACALENDRIER paca ON paca.PACM_ID = pacm.ID 
	LEFT JOIN GAHFLD.TCALENDRIERDESCRIPTIF cafo on cafo.ID = paca.CALENDRIERFOURNISSEUR_ID 
	LEFT JOIN GAHFLD.TPERIODEDACTIVITE pa ON pds.ID = pa.AFFECTATION_ID
	LEFT JOIN GAHFLD.TMATERIEL mat ON pa.MATERIEL_ID = mat.ID
	LEFT JOIN GAHFLD.TTYPEMATERIEL tmat ON mat.TYPEMATERIEL_ID = tmat.ID
	LEFT JOIN GAHFLD.TPROGRAMME prog ON mat.ID = prog.COMPTEUR_ID
	LEFT JOIN GAHFLD.TDECLINAISONGEOGRAPHIQUE dgp ON prog.DECLINAISONGEO_ID = dgp.ID
	LEFT JOIN GAHFLD.MV_TDONNEEGEOGRAPHIQUE dgeo ON edl.ADRESSE_ID = dgeo.ID
	LEFT JOIN GAHFLD.TDONNEESPROGRAMMATIONRELEVE prog_rlv ON pds.ID = prog_rlv.POINTDESERVICE_ID
WHERE 1=1
	AND ctr.DATEFIN IS NULL
	AND ctr.EXTRAITSERVICESSOUSCRIT <> 'injection'
	AND srv.DATEFIN IS NULL
	AND pacm.DATEFIN IS NULL
	AND paca.DATEFIN IS NULL
	AND pa.DATEHEUREFIN IS NULL
	AND prog.DATEFIN IS NULL
	AND srv.ROLE = 'com.hermes.crm.contrat.businessobject.ServiceSouscritAcheminementElecBTInf36'
	AND pa.MATERIEL_ROLE LIKE 'com.hermes.ref.materiel.businessobject.Compteur%'
	--AND pa.MATERIEL_ROLE NOT LIKE 'com.hermes.ref.materiel.businessobject.CompteurAMM%'
	AND pds.REFERENCE = '21323299524057'
;

--Découpage territoire
SELECT
dir.CODE INSTANCE_CODE
, DECODE(dir.CODE
	, '0321','IDF'
	, '0322', 'MMN'
	, '0323','EST'
	, '0324', 'RAB'
	, '0325','MED'
	, '0326', 'SUO'
	, '0327', 'OUE'
	, '0328', 'ACL'
	, 'autre'
	) AS INSTANCE
, dt.CODE AS DR_CODE
, SUBSTR(dt.LIBELLE, 20) AS DR
FROM GAHFLD.TPOINTDESERVICE pds
JOIN GAHFLD.EDL_DECOUPAGETERRITOIRE edldt ON edldt.SOURCE = pds.ESPACEDELIVRAISON_ID
JOIN GAHFLD.TDECOUPAGETERRITOIRE dt ON (dt.ID = edldt.DEST AND dt.TYPEDECOUPAGETERRITOIRE = '3')
JOIN gahfld.DECTERRITOIRE_DECTERRITOIRE dr_dir ON dt.ID = dr_dir.SOURCE
JOIN gahfld.TDECOUPAGETERRITOIRE dir ON dr_dir.DEST = dir.ID
WHERE pds.REFERENCE = '01100144566393'
;

--Affaires, tentatives, SLA
SELECT
aff.REFERENCEEXTERNE, pds.REFERENCE as PDS, aff.REFERENCE, aff.TYPEAFFAIRE, aff.SOUSTYPE
, DECODE(aff.STATUT,
  0, 'En cours',
  1, 'Terminé',
  3, 'Abandonné', 
  4, 'À prendre en compte',
  5, 'Édité',
  7, 'CR en attente',
  8, 'En attente duplication',
  9, 'Dupliqué',
  12, 'CR en attente publication',
  15, 'CR en attente publication',
  17, 'En attente',
  18, 'Refusé',
  19, 'En cours d''abandon',
  20, 'Validé',
  null, null,
  'Statut Inconnu'
) AS STATUT
, aff.DATEEFFETSOUHAITEE, aff.ORIGINEAFFAIRE, aff.DATECREATION, aff.OBJET, aff.CODEAFFAIRE
, natop.CODE, natop.LIBELLE, natop.TYPENATUREACTION
, t.DATEEFFETSOUHAITEE, t.MODALITEINTERVENTION, DECODE(t.MODEREALISATION, 0, 'TO','SITE') as MODEREAL, t.MOTIFNONREALISATION, t.RESULTATTECHNIQUE, t.STATUT as STA_TENTATIVE
, t.CONSTATS
, DECODE (t.NIVEAUSLAPREVU,
			 0,'Urgent',
			 1,'À date',
			 2,'À date express',
			 NULL, NULL
)AS SLA
, t.DATEEMISSION, t.DATERECEPTION, t.REFERENCEEXTERNE
, dt.LIBELLE DR
FROM GAHFLD.TAFFAIRE aff
LEFT JOIN GAHFLD.TNATUREACTION natop ON  aff.NATUREOPERATION_ID = natop.ID
LEFT JOIN GAHFLD.TESPACEDELIVRAISON edl ON aff.ADRESSE_ID = edl.ID
LEFT JOIN GAHFLD.TPOINTDESERVICE pds ON edl.ID = pds.ESPACEDELIVRAISON_ID
LEFT JOIN GAHFLD.EDL_DECOUPAGETERRITOIRE edldt ON edldt.SOURCE = aff.ADRESSE_ID
LEFT JOIN GAHFLD.TDECOUPAGETERRITOIRE dt ON dt.ID = edldt.DEST
LEFT JOIN GAHFLD.TTENTATIVE t ON  aff.ID = t.INTERVENTION_ID
WHERE 1=1
AND dt.TYPEDECOUPAGETERRITOIRE = '3'
AND aff.DATECREATION > TO_DATE('10/10/2018 00:00', 'dd/mm/yyyy hh24:mi')
AND aff.DATECREATION < TO_DATE('11/10/2018 00:00', 'dd/mm/yyyy hh24:mi')
AND aff.SOUSTYPE IN ('MSSERV','REPRISE','COUPURE','SSCRIPT') 
AND aff.REFERENCEEXTERNE IS NOT NULL
AND aff.STATUT = 1
--AND aff.REFERENCEEXTERNE = 'A03U2HGL'
ORDER BY aff.REFERENCEEXTERNE, t.DATEEMISSION
;

--Échanges Ginko
WITH ech as (
SELECT ech.ID
,ech.DATECREATION
,cast(substr(substr(jms.MESSAGECONTENT,instr(jms.MESSAGECONTENT,'<ns1:IdPrm>')),12,instr(substr(jms.MESSAGECONTENT,instr(jms.MESSAGECONTENT,'<ns1:IdPrm>')),'</ns1:IdPrm>')-12)as varchar(20)) AS REF_PDS
,cast(substr(substr(substr(jms.MESSAGECONTENT,instr(jms.MESSAGECONTENT,'<ns1:IdExtDemande>')),19,instr(substr(jms.MESSAGECONTENT,instr(jms.MESSAGECONTENT,'<ns1:IdExtDemande>')),'</ns1:IdExtDemande>')-19), 0,7) as varchar(20)) AS REF_AFF
,cast(substr(substr(jms.MESSAGECONTENT,instr(jms.MESSAGECONTENT,'<ns1:IdDemande>')),16,instr(substr(jms.MESSAGECONTENT,instr(jms.MESSAGECONTENT,'<ns1:IdDemande>')),'</ns1:IdDemande>')-16)as varchar(20)) AS REF_LKY
,cast(substr(substr(jms.MESSAGECONTENT,instr(jms.MESSAGECONTENT,'<ns0:Statut>')),13,instr(substr(jms.MESSAGECONTENT,instr(jms.MESSAGECONTENT,'<ns0:Statut>')),'</ns0:Statut>')-13)as varchar(20)) AS RESULTAT
,cast(substr(substr(jms.MESSAGECONTENT,instr(jms.MESSAGECONTENT,'<ns0:Code>')),11,instr(substr(jms.MESSAGECONTENT,instr(jms.MESSAGECONTENT,'<ns0:Code>')),'</ns0:Code>')-11)as varchar(20)) AS CODE
FROM gahfld.TECHANGE ech, gahfld.TMESSAGEPUBJMS jms
WHERE 1=1
AND ech.MESSAGE_ID = jms.ID
AND ech.MODELE_ID = 'MDB_CompteRenduProgrammerCompteurLinky_V2'
AND ech.DATECREATION >= to_date ('24/10/2018 00:00:00', 'DD/MM/YYYY HH24:MI:SS')
AND ech.DATECREATION <= to_date ('30/10/2018 00:00:00', 'DD/MM/YYYY HH24:MI:SS')
)

SELECT ech.ID, TRUNC(ech.DATECREATION) DATECREATION, ech.REF_PDS, aff.REFERENCEEXTERNE, aff.CODEAFFAIRE
, DECODE(aff.STATUT,
  0, 'En cours',
  1, 'Terminé',
  3, 'Abandonné', 
  4, 'À prendre en compte',
  5, 'Édité',
  7, 'CR en attente',
  8, 'En attente duplication',
  9, 'Dupliqué',
  12, 'CR en attente publication',
  15, 'CR en attente publication',
  17, 'En attente',
  18, 'Refusé',
  19, 'En cours d''abandon',
  20, 'Validé',
  null, null,
  'Statut Inconnu'
) AS STATUT
,ech.RESULTAT, ech.CODE, dt.LIBELLE DR
FROM ech
JOIN GAHFLD.TPOINTDESERVICE pds ON ech.REF_PDS = pds.REFERENCE
JOIN GAHFLD.TAFFAIRE aff ON ech.REF_AFF = aff.REFERENCE
JOIN GAHFLD.EDL_DECOUPAGETERRITOIRE edldt ON edldt.SOURCE = pds.ESPACEDELIVRAISON_ID
JOIN GAHFLD.TDECOUPAGETERRITOIRE dt ON dt.ID = edldt.DEST
WHERE dt.TYPEDECOUPAGETERRITOIRE = '3'
AND ech.REF_PDS = '21307525193459'
;

--Point, interlocuteurs
SELECT pds.REFERENCE
, DECODE(pds.ETAT,
		  '1', 'ne peut être mis en service',
		  '3', 'hors service',
		  '4', 'en service',
		  '5', 'supprimé',
		  '12', 'non raccordable',
		  '13', 'raccordable',
		  'inconnu') as ETAT
		  , modrolact.LIBELLE
		  --, actedl.NOM OCCUPANT_NOM, actedl.COMPLEMENTNOM OCCUPANT_PRENOM
		  , actrat.NOM RAT_NOM, actrat.COMPLEMENTNOM RAT_PRENOM
		  , aprat.CODEPOSTAL, aprat.COMMUNE, aprat.ESPACEDELIVRAISON_ID EDL_ID, aprat.NUMERO, aprat.VOIE
FROM GAHFLD.TESPACEDELIVRAISON edl
JOIN GAHFLD.TPOINTDESERVICE pds ON edl.ID = pds.ESPACEDELIVRAISON_ID
JOIN GAHFLD.EDL_DECOUPAGETERRITOIRE edldt ON edldt.SOURCE = pds.ESPACEDELIVRAISON_ID
JOIN GAHFLD.TDECOUPAGETERRITOIRE dt ON dt.ID = edldt.DEST
--JOIN GAHFLD.TADRESSEPOSTALE apedl ON edl.ID = apedl.ESPACEDELIVRAISON_ID
--JOIN GAHFLD.TACTEUR actedl ON actedl.ADRESSEPOSTALE_ID = apedl.ID
JOIN GAHFLD.CONTRAT_ESPACESDELIVRAISON ce ON edl.ID = ce.DEST
JOIN GAHFLD.TCONTRAT ctr ON ce.SOURCE = ctr.ID
--JOIN GAHFLD.TROLE rol ON ctr.TITULAIRE_ID = rol.ID
--JOIN GAHFLD.TACTEUR actctr ON rol.ACTEUR_ID = actctr.ID
JOIN GAHFLD.TROLEACTEUR rolact ON (rolact.OBJETMAITRE_ID = ctr.ID AND rolact.OBJETMAITRE_ROLE = 'com.hermes.crm.contrat.businessobject.Contrat')
JOIN GAHFLD.TMODELEROLEACTEUR modrolact ON modrolact.ID = rolact.MODELEROLEACTEUR_ID
JOIN GAHFLD.TACTEUR actrat ON actrat.ID = rolact.ACTEUR_ID
JOIN GAHFLD.TADRESSEPOSTALE aprat ON aprat.ID = actrat.ADRESSEPOSTALE_ID
WHERE 1=1
AND dt.TYPEDECOUPAGETERRITOIRE = '2'
AND dt.LIBELLE = 'CCD/DR/DIR 235/3263-NMP/0326 - Aveyron Lozère'
--AND aprat.TYPEADRESSEPOSTALE = '2'
--AND pds.REFERENCE = '16542546991535'
;

--SMO actifs
SELECT pds.REFERENCE, srv.LIBELLECOURT, srvs.DATEDEBUTPREVUE, srvs.DATEFINPREVUE
	, DECODE (srvs.TYPEDEMANDEUR,
		 0, 'Fournisseur',
		 1, 'Fournisseur Tiers',
		 2, 'Client',
		 3, 'Interne',
		 4, 'Tiers autorisé',
		 srvs.TYPEDEMANDEUR
		) DEMANDEUR
FROM GAHFLD.TPOINTDESERVICE pds
JOIN GAHFLD.TSERVICESOUSCRIT srvs ON pds.ID = srvs.POINTDESERVICE_ID
JOIN GAHFLD.TSERVICE srv ON srvs.SERVICE_ID = srv.ID
WHERE 1=1
AND srvs.TYPEDEMANDEUR IS NOT NULL
AND srv.LIBELLECOURT LIKE 'CDC%'
AND srvs.DATEFIN IS NULL

--SMO actifs + publication + demandeurs
SELECT pds.REFERENCE, srv.LIBELLECOURT, srvs.DATEDEBUTPREVUE, srvs.DATEFINPREVUE
	, DECODE (srvs.TYPEDEMANDEUR,
		 0, 'Fournisseur',
		 1, 'Fournisseur Tiers',
		 2, 'Client',
		 3, 'Interne',
		 4, 'Tiers autorisé',
		 srvs.TYPEDEMANDEUR
		) DEMANDEUR,
	CASE WHEN srvs.TYPEDEMANDEUR = 2 THEN DECODE (nvl(act1.EMAIL,''),'','NON','OUI') ELSE DECODE (nvl(act2.EMAIL,''),'','NON','OUI') END PORTAIL,
	DECODE (substr(srv.libellecourt,6),
		 'JO', 'Journalière',
		 'ME', 'Mensuelle',
		 'XX'
		) PUBLICATION,
	CASE WHEN srvs.TYPEDEMANDEUR = 3 THEN act1.NOM END SI_DEMANDEUR
FROM GAHFLD.TSERVICESOUSCRIT srvs,
	GAHFLD.TPOINTDESERVICE pds,
	GAHFLD.TSERVICE srv,
	GAHFLD.TACTEUR act1,
	GAHFLD.TACTEUR act2,
	GAHFLD.TCONTRAT ctr,
	GAHFLD.TPOINTACCESSERVICESCLIENT pdsclient,
	GAHFLD.TROLEACTEUR rolact,
	GAHFLD.TMODELEROLEACTEUR modrolact
WHERE srvs.TYPEDEMANDEUR IS NOT NULL
	AND srvs.POINTDESERVICE_ID = pds.ID
	AND srvs.SERVICE_ID = srv.ID
	AND ctr.POINTACCESSERVICESCLIENT_ID = pdsclient.ID
	AND pdsclient.POINTDESERVICE_ID = pds.ID
	AND rolact.OBJETMAITRE_ID = ctr.ID
	AND act2.ID = rolact.ACTEUR_ID
	AND ctr.STATUTEXTRAIT = 1
	AND rolact.MODELEROLEACTEUR_ID = modrolact.ID
	AND modrolact.LIBELLE = 'titulaire contrat de fourniture'
	AND srv.LIBELLECOURT LIKE 'CDC%'
	AND srvs.DEMANDEUR_ID = act1.id (+)
	AND ctr.DATEFIN IS NULL
	AND srvs.DATEFIN IS NULL
;

--C15
SELECT DISTINCT pds.REFERENCE as PDS
, aff.REFERENCEEXTERNE as AFFAIRE
, aff.SOUSTYPE
, op.LIBELLE
, trunc(aff.DATECREATION) as DATECREATION
, ech.DATEMODIFICATION as DATE_ECHANGE
FROM gahfld.TAFFAIRE aff
INNER JOIN GAHFLD.TESPACEDELIVRAISON edl ON edl.ID = aff.adresse_id
INNER JOIN gahfld.TPOINTDESERVICE pds ON pds.ESPACEDELIVRAISON_ID = edl.ID
INNER JOIN gahfld.TSERVICESOUSCRIT ss ON (ss.POINTDESERVICE_ID = pds.ID AND ss.STATUT = 1)
INNER JOIN gahfld.TCONTRAT c ON c.ID = ss.CONTRAT_ID
INNER JOIN gahfld.TOFFREPRODUIT op ON op.ID = c.OFFREPRODUIT_ID
INNER JOIN gahfld.TAFFAIRE aff ON (aff.ADRESSE_ID = edl.ID and aff.ROLE = 'com.hermes.itv.intervention.businessobject.InterventionElectricite' AND aff.SousType not in ('ACTCDC','DESCDC','AER','RER'))
INNER JOIN gahfld.TECHANGE ech ON (ech.OBJETMAITRE_ID = aff.ID AND ech.MODELE_ID = 'ME_PUB_INT_AFF_450')
WHERE 1=1
AND (
	aff.REFERENCEEXTERNE IN ('A04437JW')
	)


--Relève
SELECT COMMENTAIRERELEVEUR, PDS, DTR, DATE_RELEVE_PROGRAMMEE, HEUREDEBUTPLAGEPASSAGERELEVEUR, HEUREFINPLAGEPASSAGERELEVEUR, STATUT_CONTRAT, NUMERO_EDL, "Type voie edl", VOIE_EDL, COMMUNE_EDL, CODE_POSTAL_EDL, LIGNE5COMPLEMENT, NOM, PRENOM, TELEPHONEMOBILE, TELEPHONEFIXE, EMAIL, LIGNE2LOCAL, LIGNE3BATIMENT, NUMERO, VOIE, CODEPOSTAL, COMMUNE, rang_role_occ_desc, "Campagne", "Statut Campagne", "Statut EDP Relève", "Mode collecte relève", "Circuit", DR, "Réf. marché prestataire", "Réf. prestataire", COMMENTAIRE_PRERELV
FROM (
		  SELECT /*+ LEADING(echeance) PARALLEL(8) USE_NL(pds, edp_releve) */
		  pds.REFERENCE AS PDS
		  , pds.COMMENTAIRERELEVEUR
		  , CASE WHEN (lot.MODELEDELOT_ROLE = 'com.hermes.itv.releve.businessobject.ModeleDeLotDeReleveParTSP') THEN echeance.DATEEXECUTIONPREVUE + 18 ELSE echeance.DATEEXECUTIONPREVUE + 2 END AS DTR
		  , donnees_prog_releve.DATERELEVEPROGRAMMEE AS DATE_RELEVE_PROGRAMMEE, to_char(donnees_prog_releve.HEUREDEBUTPLAGEPASSAGERELEVEUR, 'HH24:MI:SS') AS HEUREDEBUTPLAGEPASSAGERELEVEUR, to_char(donnees_prog_releve.HEUREFINPLAGEPASSAGERELEVEUR, 'HH24:MI:SS') AS HEUREFINPLAGEPASSAGERELEVEUR, decode(contrat.STATUTEXTRAIT, 0, 'souscription', 1, 'actif', 4, 'cessé') AS STATUT_CONTRAT, geo.NUMEROVOIE AS NUMERO_EDL, geo.TYPEVOIE AS "Type voie edl", geo.VOIE AS VOIE_EDL, geo.COMMUNE AS COMMUNE_EDL, lpad(geo.CODE_POSTAL,5,'0') AS CODE_POSTAL_EDL, edl.COMPLEMENTLOCALISATION AS LIGNE5COMPLEMENT, occupant."Nom occupant" AS NOM, occupant."Prénom occupant" AS PRENOM, occupant."Téléphone 1 occupant" AS TELEPHONEMOBILE, occupant."Téléphone 2 occupant" AS TELEPHONEFIXE, occupant."Email occupant" AS EMAIL, occupant."Libellé - appt - étage occup." AS LIGNE2LOCAL, occupant."Entrée / escalier occupant" AS LIGNE3BATIMENT, occupant."Numéro voie occupant" AS NUMERO, occupant."Voie occupant" AS VOIE, occupant."Code postal occupant" AS CODEPOSTAL, occupant."Commune occupant" AS COMMUNE, occupant.rang_role_occ_desc, campagne.LIBELLE AS "Campagne"
		  , DECODE(campagne.STATUT, 0, 'en cours',
				1, 'fermé',
				2, 'annulé',
				3, 'suspendu',
				4, 'suppression en cours',
				'inconnu') AS "Statut Campagne"
		, DECODE(edp_releve.STATUT,
				0, 'sélectionné',
				1, 'écarté',
				2, 'en cours relève',
				3, 'relevé',
				4, 'absent relève',
				8, 'absent relève technique',
				5, 'traité',
				6, 'à estimer',
				7, 'estimé',
				10, 'complément à estimer',
				11, 'relevé et estimé complémentaire',
				999, 'mis en lot d’isolés') AS "Statut EDP Relève"
		  , mode_gestion_zone_releve.MODECOLLECTERELEVE AS "Mode collecte relève", donnees_prog_releve.REFERENCECIRCUIT AS "Circuit", substr(dr.LIBELLE, 20) AS DR, mode_gestion_zone_releve.REFERENCEMARCHEPRESTATAIRE AS "Réf. marché prestataire", mode_gestion_zone_releve.REFERENCEPRESTATAIRE AS "Réf. prestataire"
		  , substr(pds.COMMENTAIRERELEVEUR, instr(pds.COMMENTAIRERELEVEUR, 'PRERELEV', 1, 1) + 8, instr(pds.COMMENTAIRERELEVEUR, 'PRERELEV', 1, 2) - (instr(pds.COMMENTAIRERELEVEUR, 'PRERELEV', 1, 1)+8)) AS COMMENTAIRE_PRERELV
		  , DENSE_RANK() OVER (PARTITION BY pds.REFERENCE ORDER BY service_souscrit.DATEFIN desc, service_souscrit.DATEEFFET desc, service_souscrit.STATUT, service_souscrit.DATEMODIFICATION) AS rang_service_desc
		  FROM gahfld.TELEMENTDEPOPULATIONRELEVE edp_releve
		  JOIN gahfld.TPOINTDESERVICE pds ON edp_releve.POINTDESERVICE_ID = pds.ID
			 AND mod(pds.ETATOBJET,2) = 0
		  JOIN gahfld.TLOT lot ON edp_releve.LOT_ID = lot.ID
			 AND mod(edp_releve.ETATOBJET,2) = 0
		  JOIN gahfld.TCAMPAGNE campagne ON lot.CAMPAGNE_ID = campagne.ID
			 AND mod(campagne.ETATOBJET,2) = 0
		  JOIN gahfld.TECHEANCE echeance ON campagne.ECHEANCEDECLENCHEE_ID = echeance.ID
			 AND mod(echeance.ETATOBJET,2) = 0
		  JOIN gahfld.TESPACEDELIVRAISON edl ON pds.ESPACEDELIVRAISON_ID = edl.ID
			 AND mod(edl.ETATOBJET,2) = 0
			 AND mod(pds.ETATOBJET, 2) = 0
			 AND pds.ROLE = 'com.hermes.ref.edl.businessobject.PointDeServiceElectricite'
		  JOIN gahfld.VRS_DONNEEGEOGRAPHIQUE geo ON edl.ADRESSE_ID = geo.ID
		  JOIN gahfld.CONTRAT_ESPACESDELIVRAISON contrat_edl ON edl.ID = contrat_edl.DEST
		  JOIN gahfld.TCONTRAT contrat ON contrat_edl.SOURCE = contrat.ID
		  JOIN gahfld.EDL_DECOUPAGETERRITOIRE edl_secteur ON edl.ID = edl_secteur.SOURCE
		  JOIN gahfld.TDECOUPAGETERRITOIRE secteur ON edl_secteur.DEST = secteur.ID
			 AND mod(secteur.ETATOBJET,2) = 0
			 AND secteur.TYPEDECOUPAGETERRITOIRE = 1
			 AND secteur.LIBELLE NOT LIKE '%Secteur fictif%'
		  JOIN gahfld.DECTERRITOIRE_DECTERRITOIRE secteur_centre ON secteur.ID = secteur_centre.SOURCE
		  JOIN gahfld.TDECOUPAGETERRITOIRE centre ON secteur_centre.DEST = centre.ID
		  JOIN gahfld.DECTERRITOIRE_DECTERRITOIRE centre_dr ON centre.ID = centre_dr.SOURCE
		  JOIN gahfld.TDECOUPAGETERRITOIRE dr ON centre_dr.DEST = dr.ID
			 AND dr.CODE = dr.CODE
		  JOIN gahfld.DECTERRITOIRE_DECTERRITOIRE dr_dir ON dr.ID = dr_dir.SOURCE
		  JOIN gahfld.TDECOUPAGETERRITOIRE dir ON dr_dir.DEST = dir.ID
		  LEFT JOIN (
					 SELECT * FROM (
						  SELECT role_occupant.OBJETMAITRE_ID AS OBJETMAITRE_ID_OCC, occupant.INTITULE AS "Intitulé occupant", occupant.NOM AS "Nom occupant", occupant.COMPLEMENTNOM AS "Prénom occupant", occupant.TELEPHONEFIXE AS "Téléphone 1 occupant", occupant.TELEPHONEMOBILE AS "Téléphone 2 occupant", occupant.EMAIL AS "Email occupant", occupant.EMAIL2 AS "Email autre occupant", adresse_occupant.LIGNE2LOCAL AS "Libellé - appt - étage occup.", adresse_occupant.LIGNE3BATIMENT AS "Entrée / escalier occupant", adresse_occupant.NUMERO AS "Numéro voie occupant", adresse_occupant.VOIE AS "Voie occupant", adresse_occupant.LIGNE5COMPLEMENT AS "Lieu-dit/mention distr. occup.", lpad(adresse_occupant.CODEPOSTAL, 5, '0') AS "Code postal occupant", adresse_occupant.COMMUNE AS "Commune occupant", DENSE_RANK() OVER (PARTITION BY role_occupant.OBJETMAITRE_ID ORDER BY role_occupant.DATEFIN desc) AS rang_role_occ_desc
						  FROM gahfld.TROLEACTEUR role_occupant
						  JOIN gahfld.TACTEUR occupant ON role_occupant.ACTEUR_ID = occupant.ID
							 AND role_occupant.OBJETMAITRE_ROLE = 'com.hermes.ref.edl.businessobject.EspaceDeLivraison'
							 AND mod(role_occupant.ETATOBJET,2) = 0
						  LEFT JOIN gahfld.TADRESSEPOSTALE adresse_occupant ON occupant.ADRESSEPOSTALE_ID = adresse_occupant.ID
							 AND mod(adresse_occupant.ETATOBJET,2)=0
						  )
					 WHERE rang_role_occ_desc = 1) occupant
				ON edl.ID = occupant.OBJETMAITRE_ID_OCC
		  LEFT JOIN (
					 SELECT role_titulaire.OBJETMAITRE_ID AS OBJETMAITRE_ID_TIT, titulaire.NOM AS "Nom titulaire", titulaire.COMPLEMENTNOM AS "Prénom titulaire", titulaire.TELEPHONEFIXE AS "Téléphone 1 titulaire", titulaire.TELEPHONEMOBILE AS "Téléphone 2 titulaire", titulaire.EMAIL AS "Email titulaire", titulaire.EMAIL2 AS "Email autre titulaire", adresse_titulaire.LIGNE2LOCAL AS "Libellé - appt - étage titul.", adresse_titulaire.LIGNE3BATIMENT AS "Entrée / escalier titulaire", adresse_titulaire.NUMERO AS "Numéro voie titulaire", adresse_titulaire.VOIE AS "Voie titulaire", adresse_titulaire.LIGNE5COMPLEMENT AS "Lieu-dit/mention distr. titul.", lpad(adresse_titulaire.CODEPOSTAL, 5, '0') AS "Code postal titulaire", adresse_titulaire.COMMUNE AS "Commune titulaire"
					 FROM gahfld.TCONTRAT contrat, gahfld.TROLEACTEUR role_titulaire, gahfld.TMODELEROLEACTEUR modele_role_acteur, gahfld.TACTEUR titulaire, gahfld.TPERSONNEPHYSIQUE personne_phys_titulaire, gahfld.TADRESSEPOSTALE adresse_titulaire
					 WHERE contrat.ID = role_titulaire.OBJETMAITRE_ID
					 AND role_titulaire.OBJETMAITRE_ROLE = 'com.hermes.crm.contrat.businessobject.Contrat'
					 AND mod(role_titulaire.ETATOBJET,2) = 0
					 AND role_titulaire.MODELEROLEACTEUR_ID = modele_role_acteur.ID
					 AND modele_role_acteur.LIBELLE = 'titulaire contrat de fourniture'
					 AND mod(modele_role_acteur.ETATOBJET,2) = 0
					 AND role_titulaire.ACTEUR_ID = titulaire.ID
					 AND titulaire.ROLE = 'com.hermes.ref.acteur.businessobject.PersonneMorale'
					 AND mod(titulaire.ETATOBJET,2) = 0
					 AND titulaire.ID = personne_phys_titulaire.ID(+)
					 AND titulaire.ADRESSEPOSTALE_ID = adresse_titulaire.ID(+)
					 AND mod(adresse_titulaire.ETATOBJET(+),2)=0
				) titulaire_contrat
				ON contrat.ID = titulaire_contrat.OBJETMAITRE_ID_TIT
		  JOIN gahfld.UNITEFONCTIONNELLE_GEOAREAS unite_fonctionnelle_geo ON secteur.ID = unite_fonctionnelle_geo.DEST
		  JOIN gahfld.TUNITEFONCTIONNELLE unite_fonctionnelle ON unite_fonctionnelle_geo.SOURCE = unite_fonctionnelle.ID
			 AND mod(unite_fonctionnelle.ETATOBJET,2) = 0
			 AND unite_fonctionnelle.ROLE = 'com.hermes.ref.unitefonctionnelle.businessobject.PortefeuillePDS'
		  JOIN gahfld.TMODEGESTIONZONEDERELEVE mode_gestion_zone_releve ON unite_fonctionnelle.ID = mode_gestion_zone_releve.PORTEFEUILLEPDSZONEDERELEVE_ID
			 AND mod(mode_gestion_zone_releve.ETATOBJET,2) = 0
			 AND mode_gestion_zone_releve.DATEFIN IS NULL
		  JOIN gahfld.TDONNEESPROGRAMMATIONRELEVE donnees_prog_releve ON pds.ID = donnees_prog_releve.POINTDESERVICE_ID
		  JOIN gahfld.TSERVICESOUSCRIT service_souscrit ON contrat.ID = service_souscrit.CONTRAT_ID
			 AND mod(service_souscrit.ETATOBJET, 2) = 0
			 AND service_souscrit.DIRECTEUR = 1
		  WHERE (lot.MODELEDELOT_ROLE = 'com.hermes.itv.releve.businessobject.ModeleDeLotDeReleveParTSP')
		  AND campagne.STATUT = 0
		  AND mode_gestion_zone_releve.MODECOLLECTERELEVE = 0
		  --AND donnees_prog_releve.DATERELEVEPROGRAMMEE BETWEEN trunc(sysdate) + 7 AND trunc(sysdate) + 14
		  )
WHERE rang_service_desc = 1
AND COMMENTAIRERELEVEUR LIKE '%PRER%'
--AND COMMENTAIRE_PRERELV IS NOT NULL
;
	
--Recherche tables
SELECT * FROM ALL_TAB_STATISTICS
WHERE 1=1
AND NUM_ROWS > 1000
AND OWNER = 'GAHFLD'
AND TABLE_NAME IN(
  SELECT TABLE_NAME FROM ALL_TAB_COLUMNS
  WHERE COLUMN_NAME LIKE '%CALENDRIER_ID%'
)
ORDER BY 2
;

--Infos SMO CDC
SELECT pds.REFERENCE POINT
, srv.LIBELLECOURT
, substr(srv.LIBELLECOURT, 4, 2) as PAS
, srvs.REFERENCE
, srvs.STATUT
, DECODE(srvs.STATUT,
	'0', 'souscription',
	'1', 'actif',
	'3', 'cessation',
	'4', 'cessé',
	'8', 'annulé',
	'inconnu') as STATUT
, DENSE_RANK() OVER (PARTITION BY pds.REFERENCE ORDER BY srv.LIBELLECOURT, srvs.DATEEFFET DESC, srvs.REFERENCE DESC) as RANG
FROM GAHFLD.TPOINTDESERVICE pds
JOIN GAHFLD.TSERVICESOUSCRIT srvs ON pds.ID = srvs.POINTDESERVICE_ID
JOIN GAHFLD.TSERVICE srv ON srvs.SERVICE_ID = srv.ID
WHERE 1=1
AND srvs.TYPEDEMANDEUR IS NOT NULL
AND srv.LIBELLECOURT LIKE 'CDC%'
AND srvs.STATUT NOT IN ('3', '4', '8')
AND pds.REFERENCE LIKE '211%'
AND pds.REFERENCE = '21128075229925'
