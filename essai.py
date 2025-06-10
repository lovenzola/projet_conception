from sqlalchemy import create_engine, MetaData, Table, bindparam, insert
# Connexion à la base de données
engine= create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
connection= engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)
from base_donnees.etudiant import enregistrer_etudiant

#enregistrer_etudiant(
   # nom="kitenge",
   # postnom="lukusa",
   # prenom="ephraim",
   # matricule="th657423",
   # promotion="l1 lmd theologie",
   # sexe="m",
  #  date_naissance="2006-08-05"
#) 

from base_donnees.paiement import enregistrer_paiement
##enregistrer_paiement(
   # id_etudiant=5,
   # montant=870
#)

from base_donnees.etudiant import afficher_etudiant

selection = afficher_etudiant()
print (selection)

from base_donnees.historique import affichage_paiement, total_par_etudiant

affiche= affichage_paiement()
print(affiche)

totaux= total_par_etudiant()
print(totaux)


from base_donnees.paiement import frais_maximal, paiements
from base_donnees.etudiant import etudiants
maximum= frais_maximal("AE759898")
print(f"{1000- maximum}")

from sqlalchemy import select,func
maximal= frais_maximal("si")
essai= (select(
   etudiants.c.nom,
   func.sum(paiements.c.montant).label('total_paye')
).join(paiements, paiements.c.id_etudiant== etudiants.c.id )
.group_by(paiements.c.id_etudiant,etudiants.c.nom))

with engine.connect() as connection:
   for row in connection.execute(essai):
      if essai.c.total_paye > maximal:
         print("Montant paye superieur")
      else:
         print("bof")