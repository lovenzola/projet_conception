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
reconception = Table('reconception',metadata,autoload_with=engine, schema='public')
def verification_reconception(etudiant_id):
    try:
        comptage= select(func.count()).select_from(reconception).where(reconception.c.etudiant_id == etudiant_id)
        with engine.connect() as connection:
            resultat= connection.execute(comptage)
            nbre_conception= resultat.scalar()
            if nbre_conception < 3:     
                return True
            else:
                return False
    except SQLAlchemyError as e :
        print("Erreur survenue lors de l'execution de la requete:",e)
        return False
    
#-------------------------------------------------------------------------------------------------------------------------
#                         ENREGISTREMENT DANS LA TABLE RECONCEPTION
#------------------------------------------------------------------------------------------------------------------------
def save_reconception(id_etudiant):
    try:
        insertion= reconception.insert().values(etudiant_id = id_etudiant)
        with engine.connect() as connection:
            connection.execute(insertion)
            connection.commit()
    except SQLAlchemyError as e:
        print("Erreur survenue lors de l'enregistrement: ",e)
#------------------------------------------------------------------------------------------------------------------------
#                                   FONCTION DE RECONCEPTION
#------------------------------------------------------------------------------------------------------------------------
from modeles_carte.modeles_reconception import modele_fase,modele_fasi,modele_droit,modele_med
from base_donnees.etudiant import etudiants
def reconcevoir():
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
                reconception.c.etudiant_id
            ).join(etudiants, etudiants.c.id == reconception.c.etudiant_id)
            with engine.connect() as connection:
                resultat= connection.execute(requete)
                for row in resultat:
                    if verification_reconception(row.etudiant_id):
                        prefix = row.matricule[:2]
                        if prefix == "si":
                            modele = "modele_fasi"
                            modele_fasi(row)
                        elif prefix == "ae":
                            modele = "modele_fase"
                            modele_fase(row)
                        elif prefix == "dr":
                            modele = "modele_droit"
                            modele_droit(row)
                        elif prefix == "md":
                            modele = "modele_medecine"
                            modele_med(row)
                        elif prefix == "th":
                            print("Modèle pour théologie en cours de conception")
                            continue
                        else:
                            print(f"Matricule invalide : {row.matricule}")
                            continue
                        save_reconception(row.etudiant_id)
                    else:
                        print("Impossible de reconcevoir !")
    except SQLAlchemyError as e:
        print("Erreur survenue lors de la reconception:")         



