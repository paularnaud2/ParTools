--Requete EDF Commerce Hebdo et quotidienne à partir du 14 décembre
select p.prm, s.type_offre TYPE_OFFRE_ACTUEL, 
  case nvl(s.contrat,'NULL')  
    when 'PROTOC-501' then s.contrat
    when 'GRD-F003' then s.contrat
    when 'NULL' then s.contrat
  else 'AUTRE_FR' end CONTRAT_FR_ACTUEL
,
 case nvl(a.fournisseur,'NULL')  
    when 'EDF Commerce' then a.fournisseur
    when 'NULL' then a.fournisseur
  else 'AUTRE_FR' end FR_CIBLE
, a.type_offre TYPE_OFFRE_CIBLE, a.prestation , a.affaire, a.DATE_DEMANDE,a.DATE_EFFET_SOUHAITEE, a.DATE_EFFET_PREVUE DATE_EFFET, a.statut, a.ETAT_EXTERNE , 
case nvl(a.fournisseur,'NULL')  
    when 'EDF Commerce' then a.ref_demandeur
    when 'NULL' then a.fournisseur
  else ' ' end REF_DEMANDEUR,
  case nvl(a.fournisseur,'NULL')  
    when 'EDF Commerce' then a.ref_regroupement
    when 'NULL' then a.fournisseur
  else ' ' end REF_REGROUPEMENT,
  case nvl(a.fournisseur,'NULL')  
    when 'EDF Commerce' then a.uti_login
    when 'NULL' then a.fournisseur
  else ' ' end initiateur_login,
  case nvl(a.fournisseur,'NULL')  
    when 'EDF Commerce' then a.uti_civ || ' ' ||a.UTI_NOM ||' '|| a.UTI_PRENOM
    when 'NULL' then a.fournisseur
  else ' ' end   initiateur_demande
from perimetre p
left join sge s on s.prm=p.prm
left join aff a on a.prm=p.prm
WHERE 1=1
AND p.PRM LIKE '@@RG_PRM_2@@%'