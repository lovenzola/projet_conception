
from sqlalchemy import create_engine, MetaData, Table, delete
from sqlalchemy.exc import SQLAlchemyError
# Connexion à la base de données
engine= create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
connection= engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)

#                                   ENREGISTREMENTS FAITS
#-----------------------------------------------------------------------------------------------------------------------------
#                               AFFICHAGE DES ETUDIANTS
#-----------------------------------------------------------------------------------------------------------------------
from sqlalchemy import select
def afficher_etudiant():
    try:
        affichage= select(etudiants).order_by(etudiants.c.id)
        with engine.connect() as connection:
            resultat= connection.execute(affichage)
            return resultat.fetchall()
    except SQLAlchemyError as e:
        print("Erreur survenue lors de l'affichage: ",e)
#---------------------------------------------------------------------------------------------------------------------
#                                      AFFICHAGE DE TOUS LES PAIEMENTS
#---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import select, join
from base_donnees.etudiant import etudiants
from base_donnees.paiement import paiements
def affichage_paiement():
    try:
        liste_total= select(
            paiements.c.id,
            etudiants.c.nom,
            etudiants.c.promotion,
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

#------------------------------------------------------------------------------------------------------------------
#                                   AFFICHAGE TABLE PRECONCEPTION
#------------------------------------------------------------------------------------------------------------------
from base_donnees.conception import preconceptions
def afficher_preconception():
    try:
        requete= select(
            preconceptions.c.id,
            etudiants.c.nom,
            etudiants.c.postnom,
            preconceptions.c.id_etudiant,
            preconceptions.c.statut,
            preconceptions.c.date,
        ).join(etudiants, etudiants.c.id == preconceptions.c.id_etudiant).order_by(preconceptions.c.date)

        with engine.connect() as connection:
            resultat= connection.execute(requete)
            return resultat.fetchall()
    except SQLAlchemyError as e:
        print("Erreur lors de l'execution de la requete")
#--------------------------------------------------------------------------------------------------------------------
#                                           CONCEPTIONS FAITES 
#---------------------------------------------------------------------------------------------------------------------
from base_donnees.conception import conception
def afficher_conception():
    try:
        modele= Table('modeles_cartes',metadata, autoload_with=engine, schema='public')
        requete= select(
            conception.c.id,
            conception.c.etudiant_id,
            etudiants.c.nom,
            etudiants.c.postnom,
            conception.c.nom_modele,
            conception.c.date_conception
            ).join(etudiants, conception.c.etudiant_id == etudiants.c.id                       
            ).join(modele, conception.c.nom_modele == modele.c.nom_modele
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
            reconception.c.tentative,
            reconception.c.date_reconception
            ).join(etudiants, reconception.c.etudiant_id == etudiants.c.id                        
            ).order_by(reconception.c.date_reconception)
        with engine.connect () as connection:
            resultat= connection.execute(requete)
            return resultat.fetchall()
    except SQLAlchemyError as e:
        print("Erreur survenue lors de l'affichage: ",e )

def supprimer_etudiant(id_etudiant):
    
    requete_existe= select(etudiants).where(etudiants.c.id == id_etudiant)
    with engine.connect() as connection:
        resultat= connection.execute(requete_existe).scalar()
        if resultat:
            requete= delete(etudiants).where(etudiants.c.id == id_etudiant)
            connection.execute(requete)
            connection.commit()
            return f'ID {id_etudiant} supprimé avec succès'
        else:
            return f'ID inexistant'
#----------------------------------------------------------------------------------------------------------------
#                                   FONCTION SECONDAIRE 
#-----------------------------------------------------------------------------------------------------------------

def supprimer_paiement(id_etudiant):
    requete_existe= select(paiements).where(paiements.c.id_etudiant == id_etudiant)
    with engine.connect() as connection:
        resultat= connection.execute(requete_existe).scalar()
        if resultat:
            requete= delete(paiements).where(paiements.c.id_etudiant == id_etudiant)
            connection.execute(requete)
            connection.commit()
            return f'ID {id_etudiant} supprimé avec succès'
        else:
            return f'ID inexistant'
    
        

