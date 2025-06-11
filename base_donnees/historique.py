from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import SQLAlchemyError
# Connexion à la base de données
engine= create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
connection= engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)

# ENREGISTREMENTS FAITS
#-----------------------------------------------------------------------------------------------------------------------------
# ENREGISTREMENT DES ETUDIANTS
#-----------------------------------------------------------------------------------------------------------------------
from sqlalchemy import select
def afficher_etudiant():
    try:
        affichage= select(etudiants).order_by(etudiants.c.id)
        with engine.connect() as connection:
            resulat= connection.execute(affichage)
            return resulat.fetchall()
    except SQLAlchemyError as e:
        print("Erreur survenue lors de l'affichage: ",e)
#---------------------------------------------------------------------------------------------------------------------
#                                           PAIEMENTS EFFECTUES
#---------------------------------------------------------------------------------------------------------------------
#                                      HISTORIQUE DE TOUS LES PAIEMENTS
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
    except SQLAlchemyError as e :
        print("Erreur lors de l'affichage: ", e)

#-------------------------------------------------------------------------------------------------------------------------
#                                           TOTAL PAYE PAR ETUDIANT
#-------------------------------------------------------------------------------------------------------------------------
from sqlalchemy import select, func
def afficher_paiement_etudiant():
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
    except SQLAlchemyError as e:
        print("Erreur survenue lors de l'affcihage:",e)
#--------------------------------------------------------------------------------------------------------------------
#                                           CONCEPTIONS FAITES 
#---------------------------------------------------------------------------------------------------------------------
from base_donnees.conception import conception
def afficher_conception():
    try:
        requete= select(
            conception.c.id,
            conception.c.etudiant_id,
            etudiants.c.nom,
            etudiants.c.postnom,
            conception.c.modele_id,
            conception.c.date_conception
            ).join(etudiants, conception.c.etudiant_id == etudiants.c.id                       
            ).order_by(conception.c.date_conception)
        with engine.connect () as connection:
            resultat= connection.execute(requete)
            return resultat.fetchall()
    except SQLAlchemyError as e:
        print("Erreur survenue lors de l'affichage: ",e )
#-------------------------------------------------------------------------------------------------------------------------
#                                   RECONCEPTIONS FAITES 
#-------------------------------------------------------------------------------------------------------------------------
from base_donnees.reconception import reconception
def afficher_reconception():
    try:
        requete= select(
            reconception.c.id,
            reconception.c.etudiant_id,
            etudiants.c.nom,
            etudiants.c.postnom,
            reconception.c.date_reconception
            ).join(etudiants, reconception.c.etudiant_id == etudiants.c.id                        
            ).order_by(reconception.c.date_reconception)
        with engine.connect () as connection:
            resultat= connection.execute(requete)
            return resultat.fetchall()
    except SQLAlchemyError as e:
        print("Erreur survenue lors de l'affichage: ",e )