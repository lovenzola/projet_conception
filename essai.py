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

from base_donnees.paiement import affichage_paiement, total_par_etudiant

affiche= affichage_paiement()
print(affiche)

totaux= total_par_etudiant()
print(totaux)
