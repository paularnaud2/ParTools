# Minutage
import common as com
import time
step_log(counter, step, what = 'lignes écrites', nb = 0, th_name = 'DEFAULT')
    # Pour une utilisation simple, initialiser avec init_sl_time()
    # Pour une utilisation multi_thread, initialiser avec gen_sl_detail(range_name)
start_time = time.time()
<traitement dont on veut mesurer la durée>
dur = com.get_duration_ms(start_time)
bn = com.big_number(counter)
s = "Injection des données terminée. {} lignes insérées en {}."
s = s.format(bn, com.get_duration_string(dur))
com.log(s)

# Basic================================================================
# Opérateurs
<	Strictement inférieur à
>	Strictement supérieur à
<=	Inférieur ou égal à
>=	Supérieur ou égal à
==	Égal à
!=	Différent de

# Incrémentation
variable += 1 # -=, *= existent aussi

# Permutation
a,b = b,a

# Aller à la ligne dans le code
    new_line = [line[fields['RAE']]\
    , line[fields['raisonSociale']]\
    , line[fields['typeCompteur']]\
    , line[fields['optionTarifaire']]]
# Au lieu de
    new_line = [line[fields['RAE']], line[fields['raisonSociale']], line[fields['typeCompteur']], line[fields['optionTarifaire']]]
    
# If=====================================================================
annee = input("Saisissez une année : ") # On attend que l'utilisateur saisisse l'année qu'il désire tester
annee = int(annee) # Risque d'erreur si l'utilisateur n'a pas saisi un nombre
bissextile = False # On crée un booléen qui vaut vrai ou faux

if annee % 400 == 0:
    bissextile = True
elif annee % 100 == 0:
    bissextile = False
else:
    bissextile = False
    
# Boucles===================================================================
# Boucle While
nb = 7 # On garde la variable contenant le nombre dont on veut la table de multiplication
i = 0 # C'est notre variable compteur que nous allons incrémenter dans la boucle
while i < 10: # Tant que i est strictement inférieure à 10
    print(i + 1, "*", nb, "=", (i + 1) * nb)
    i += 1 # On incrémente i de 1 à chaque tour de boucle
    if lettre == "Q":
        print("Fin de la boucle")
        break
    else
        continue # On retourne au while sans exécuter les autres lignes
    
# Boucle For
chaine = "Bonjour les ZER0S"
for lettre in chaine:
    if lettre in "AEIOUYaeiouy": # lettre est une voyelle
        print(lettre)
        continue # retour en haut du for
    else: # lettre est une consonne... ou plus exactement, lettre n'est pas une voyelle
        print("*")

pass # Ne rien faire dans une boucle ou un if
        
# Définition de fonction et importations======================================
def fonc(a, b):
def fonc(a=1, b=2):
fonc = lambda x, y: x + y:
import math as m
from math import sqrt
from math import *

# Module math=================================================================
import math
a = 5, b = 3
sqrt(a) # Racine carrée
fabs(a) # valeur absolue
floor(a) # Partie entière
a//b = 1 # Quotient division euclidienne
a%b = 2 # Reste division euclidienne

# Exceptions==================================================================
annee = input() # L'utilisateur saisit l'année
try:
    annee = int(annee) # On tente de convertir l'année
    if annee<=0:
        raise ValueError("l'année saisie est négative ou nulle")
except ValueError as err: # ou plus générique : except Exception as err
    print("La valeur saisie est invalide (l'année est peut-être négative).")

# Nombres aléatoires=========================================================
import random
randrange(50) # Entre 0 et 50
randrange(1,7) # Entre 1 et 6
choice(list) # Choisit un élément d'une list au hasard

# Chaînes de caractère=======================================================
chaine.lower()
chaine.upper()
len(chaine)
message = "J'ai " + age + " ans."
print("Cela s'est produit le {}, à {}.".format(date, heure))
print("Cela s'est produit le {date}, à {heure}.".format(date = "Dimanche 24 juillet 2011", heure = "17:00"))
chaine[0], chaine[0:2], chaine[:2], chaine[2:]
chaine.isalpha()
chaine.isalnum()
chaine.isdigit()
chaine.capitalize()
chaine.find(LOOK_FOR)
ma_chaine = "Bonjour à tous"
ma_chaine.split(" ") #['Bonjour', 'à', 'tous']
string.replace(old, new)
line.strip("\n") #retirer des caractères aux extremités
isinstance(row, str): #vérifie que row est de type string
datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f") # formatage date

# Listes=====================================================================
ma_liste = [1, 2, 3]
ma_liste.append(56)
ma_liste.insert(2, 'c') # On insère 'c' à l'indice 2
ma_liste1.extend(ma_liste2) # On insère ma_liste2 à la fin de ma_liste1
ma_liste1 += ma_liste2 # Identique à extend
del ma_liste[2] # On supprime le troisième élément de la liste
ma_liste.remove(32) # La méthoderemovene retire que la première occurrence de la valeur trouvée dans la liste !
ma_liste2 = list(ma_liste1) # Cela revient à copier le contenu de ma_liste1 (sinon référence à l'objet)
len(ma_list) # nombre d'élément dans la liste

for elt in ma_liste: # elt va prendre les valeurs successives des éléments de ma_liste
    print(elt)

for i, elt in enumerate(ma_liste):
    print("À l'indice {} se trouve {}.".format(i, elt))

ma_liste = ['Bonjour', 'à', 'tous']
" ".join(ma_liste)
'Bonjour à tous'

# Appel d'une fonction avec une liste de paramètres
liste_des_parametres = [1, 4, 9, 16, 25, 36]
print(*liste_des_parametres)
1 4 9 16 25 36

# Compréhension de liste
inventaire_inverse = [(qtt, nom_fruit) for nom_fruit,qtt in inventaire] # On change le sens de l'inventaire, la quantité avant le nom
inventaire_inverse.sort(reverse=True) # On trie l'inventaire inversé dans l'ordre décroissant
inventaire = [(nom_fruit, qtt) for qtt,nom_fruit in inventaire_inverse] # Et on reconstitue l'inventaire

# Trier une liste de tuples par rapport au deuxième élément des tuples
sorted(etudiants, key=lambda colonnes: colonnes[2])

# ou (plus rapide)
from operator import itemgetter
sorted(etudiants, key=itemgetter(2))

# Ensembles=================================================================
# Un ensemble est une collection non ordonnée sans élément dupliqué.
# Recherche de doublons avec set :
seen = set()
uniq = []
for x in a:
    if x not in seen:
        uniq.append(x)
        seen.add(x)

# ou avec Counter() (moins rapide)
from collections import Counter()
    a = [1,2,3,2,1,5,6,5,5,5]
    c = Counter(a)
    print ([item for item, count in c.items() if count > 1])
-> [1, 2, 5]
        

# Dictionnaires==============================================================
mon_dictionnaire = {}
mon_dictionnaire["pseudo"] = "Prolixe"
placard = {"chemise":3, "pantalon":6, "tee-shirt":7}
for cle in fruits.keys() # Parcours des clés
for valeur in fruits.values() # Parcours des valeurs
for cle, valeur in fruits.items() # Parcours des clés et des valeurs

# Appel d'une fonction avec un dictionnaire
parametres = {"sep":" >> ", "end":" -\n"}
print("Voici", "un", "exemple", "d'appel", **parametres)
Voici >> un >> exemple >> d'appel -

# Compréhension de dictionnaire
dictOfWords = { i : 5 for i in listOfStr }

# Fichiers===================================================================
import os
os.chdir("C:/tests python") # Changer le répertoire de travail courant
..\rep1\fic1.txt # Chemin relatif
mon_fichier = open("fichier.txt", "r")
    # 'r': ouverture en lecture (Read).
    # 'w': ouverture en écriture (Write). Le contenu du fichier est écrasé. Si le fichier n'existe pas, il est créé.
    # 'a': ouverture en écriture en mode ajout (Append). On écrit à la fin du fichier sans écraser l'ancien contenu du fichier. Si le fichier n'existe pas, il est créé.
mon_fichier.write("Premier test d'écriture dans un fichier via Python") # Renvoie le nombre de caractères qui ont été écrits
texte = mon_fichier.read()
mon_fichier.close()
with open('fichier.txt', 'r', encoding='utf-8') as mon_fichier: # Pas besoin d'utiliser close
    texte = mon_fichier.read() # lecture du fichier entier
    texte = mon_fichier.readline() # lecture ligne par ligne
    texte = mon_fichier.readlines() # liste ligne par ligne
for line in in_file: # lecture ligne par ligne
os.remove(FILE_OUT) # supprimer un fichier
from shutil import copyfile
copyfile(src, dst) # copie de fichier
shutil.move(src, dst) # déplacement de fichier
os.makedirs(LOG_OUT) # créer une arborescence
os.rename(source, target) # renommer un fichier
folders = [f[0] for f in os.walk(package_path)] # lister des dossiers
files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
os.path.exists(dir) # vérifier l'existence d'un fichier
os.startfile(dir) # lancer un fichier avec l'appli par défaut

# Enregistrement et chargement d'objets dans des fichiers
import pickle
with open('donnees', 'wb') as fichier: # 'wb' pour écriture binaire
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(score) # Enregistrement de l'objet score
with open('donnees', 'rb') as fichier:
    mon_depickler = pickle.Unpickler(fichier)
    score_recupere = mon_depickler.load()

# Divers=======================================================================
import sys
sys.exit() # arrêter un script
gl = __import__('reqlist.' + gl_file, fromlist=[None]) # importer un sous module avec la fonction spéciale __import__
def run_reqList(**params): # les noms/valeurs sont convertis en dictionnaire params
a = gl.__getattribute__(key) # récupérer un attribut depuis une string
gl.__setattr__(key, params[key]) # valoriser un attribut depuis une string
# Execution d'un fichier python (code venant de flask/config
with open(filename, mode="rb") as config_file:
                exec(compile(config_file.read(), filename, "exec"), d.__dict__)
# Interpreter path
sys.executable