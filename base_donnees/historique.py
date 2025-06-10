# ENREGISTREMENTS FAITS
#------------------------------------------------------------------------------------------------------------------
# ENREGISTREMENT D'ETUDIANTS
#------------------------------------------------------------------------------------------------------------------
from base_donnees.etudiant import etudiants












#---------------------------------------------------------------------------------------------------------------------
# PAIEMENTS EFFECTUES
#---------------------------------------------------------------------------------------------------------------------
# HISTORIQUE DE TOUS LES PAIEMENTS
#---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import select, join
from base_donnees.etudiant import etudiants
from base_donnees.paiement import paiements
def affichage_paiement():
    try:
        liste_total= select(
            paiements.c.id,
            etudiants.c.nom,
            etudiants.c.matricule,
            paiements.c.id_etudiant,
            paiements.c.montant,
            paiements.c.date_paiement
        ).join(
            etudiants, paiements.c.id_etudiant == etudiants.c.id).order_by(paiements.c.date_paiement)

        with engine.connect() as connection:
            resultat= connection.execute(liste_total)
            return resultat.fetchall()
    except Exception as e :
        print("Erreur lors de l'affichage: ", e)

#-------------------------------------------------------------------------------------------------------------------------
# TOTAL PAYE PAR ETUDIANT
#-------------------------------------------------------------------------------------------------------------------------
from sqlalchemy import select, func
def total_par_etudiant():
    try:
        total= (
            select(
                paiements.c.id_etudiant,
                etudiants.c.nom,
                etudiants.c.postnom,
                etudiants.c.prenom,
                func.sum(paiements.c.montant).label("total_paye")
            )
            .join(etudiants, paiements.c.id_etudiant == etudiants.c.id)
            .group_by(paiements.c.id_etudiant,etudiants.c.nom,etudiants.c.postnom,etudiants.c.prenom)
            .order_by(paiements.c.id_etudiant))
        
        with engine.connect() as connection:
            resultat= connection.execute(total)
            return resultat.fetchall()
    except Exception as e:
        print("Erreur survenue lors de l'affcihae:",e)