from sqlalchemy import create_engine, MetaData, Table,select, func
from sqlalchemy.exc import SQLAlchemyError
# Connexion à la base de données
engine= create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
connection= engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)
#------------------------------------------------------------------------------------------------------------------------
#                  CONDITION DE LA PHASE DE CONCEPTION
#------------------------------------------------------------------------------------------------------------------------
preconceptions = Table('preconception', metadata, autoload_with=engine, schema='public')
def verification_conception():
    try:
        comptage = select(func.count()).select_from(preconceptions)
        with engine.connect() as connection:
            resultat= connection.execute(comptage)
            nbre_etudiant= resultat.scalar()
            if nbre_etudiant >= 10:
                print("Nombre de paiements atteint. Voulez-vous concevoir?")
                return True
            else:
                print("Nombre de paiements inferieur à 10. Pas de conception")
                return False
    except SQLAlchemyError as e :
        print("Erreur survenue lors de la verification:",e)

#-----------------------------------------------------------------------------------------------------------------------
#                    FONCTION POUR VIDER LA TABLE PRECONCEPTION
#-----------------------------------------------------------------------------------------------------------------------
from sqlalchemy import delete
def vider_preconception():
    requete= delete(preconceptions)
    with engine.connect() as connection:
        connection.execute(requete)
        connection.commit()
#-------------------------------------------------------------------------------------------------------------------------
#       FONCTION DE CONCEPTION ET ENREGISTREMENT 
#------------------------------------------------------------------------------------------------------------------------
from base_donnees.etudiant import etudiants
from modeles_carte.modeles import modele_droit,modele_fase,modele_fasi,modele_med
conception= Table("conception",metadata, autoload_with=engine, schema="public")
modeles= Table("modeles_cartes", metadata, autoload_with=engine, schema="public")
def concevoir():
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
            preconceptions.c.id_etudiant
        ).join(etudiants, etudiants.c.id == preconceptions.c.id_etudiant)

        with engine.connect() as connection:
            resultat = connection.execute(requete)
            for row in resultat:
                # Choix du modèle
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

                # Enregistrement dans la table "conception"
                connection.execute(
                    conception.insert().values(
                        etudiant_id =row.id_etudiant,
                        nom_modele=modele
                    )
                )
            vider_preconception()
    except Exception as e:
        print(f"Erreur survenue lors de la conception : {e}")

