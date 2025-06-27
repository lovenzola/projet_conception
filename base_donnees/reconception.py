from sqlalchemy import create_engine, MetaData, Table, select, func
from sqlalchemy.exc import SQLAlchemyError
# Connexion à la base de données
engine= create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
connection= engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)
#-----------------------------------------------------------------------------------------------------------------------
#               FONCTION DE VERIFICATION DE CONCEPTION
#----------------------------------------------------------------------------------------------------------------------
conception= Table('conception',metadata, autoload_with=engine, schema='public')
reconception = Table('reconception',metadata,autoload_with=engine, schema='public')
def verification_reconception(etudiant_id):
    try:
        with engine.connect() as connection:
            verifcation_conception= select(func.count()).select_from(conception).where(conception.c.etudiant_id == etudiant_id)
            validation = connection.execute(verifcation_conception)
            if validation.scalar() == 0:
                return False
    
            comptage= select(func.count()).select_from(reconception).where(reconception.c.etudiant_id == etudiant_id)
            resultat= connection.execute(comptage)
            nbre_conception= resultat.scalar()
            if nbre_conception >=3:     
                return False
            
            return True
    except SQLAlchemyError as e :
        print("Erreur survenue lors de l'execution de la requete:",e)
        return False
    
def verifier_tentative(etudiant_id):
    try:
        requete= select(func.count()).select_from(reconception).where(reconception.c.etudiant_id == etudiant_id)

        with engine.connect() as connection:
            resultat= connection.execute(requete)
            return resultat.scalar() +1
    except SQLAlchemyError as e:
        print("Erreur lors du comptage de tentatives", e)
        return 1
#------------------------------------------------------------------------------------------------------------------------
#                                   FONCTION DE RECONCEPTION
#------------------------------------------------------------------------------------------------------------------------
from modeles_carte.modeles_reconception import modele_med_reconception,modele_fasi_reconception,modele_fase_reconception,modele_droit_reconception
from base_donnees.etudiant import etudiants
def reconcevoir(etudiant_id):
    try:
            requete = select(
                etudiants.c.matricule,
                etudiants.c.nom,
                etudiants.c.postnom,
                etudiants.c.prenom,
                etudiants.c.sexe,
                etudiants.c.promotion,
                etudiants.c.date_naissance,
                etudiants.c.photo_path,
            ).where(etudiants.c.id == etudiant_id)
           
                
            with engine.connect() as connection:
                resultat= connection.execute(requete).fetchone()
                if not resultat :
                    return
                tentative= verifier_tentative(etudiant_id)       
                if verification_reconception(etudiant_id):
                    prefix = resultat.matricule[:2]
                    if prefix == "si":
                        modele_fasi_reconception(resultat,tentative)
                    elif prefix == "ae":
                        modele_fase_reconception(resultat,tentative)
                    elif prefix == "dr":
                        modele_droit_reconception(resultat,tentative)
                    elif prefix == "md":
                        modele_med_reconception(resultat,tentative)
                    elif prefix == "th":
                        print("Modèle pour théologie en cours de conception")
            
                    else:
                        return
                    save_reconception(etudiant_id, tentative)
                else:
                        return False
    except SQLAlchemyError as e:
        print("Erreur survenue lors de la reconception:")         
#-------------------------------------------------------------------------------------------------------------------------
#                         ENREGISTREMENT DANS LA TABLE RECONCEPTION
#------------------------------------------------------------------------------------------------------------------------
def save_reconception(etudiant_id, tentative):
    try:
        insertion= reconception.insert().values(
            etudiant_id = etudiant_id,
            tentative= tentative
        )
        with engine.connect() as connection:
            connection.execute(insertion)
            connection.commit()
    except SQLAlchemyError as e:
        print("Erreur survenue lors de l'enregistrement: ",e)


