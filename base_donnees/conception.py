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

#-------------------------------------------------------------------------------------------------------------------------
#       FONCTION DE CONCEPTION AVEC REPORTLAB 
#------------------------------------------------------------------------------------------------------------------------
from sqlalchemy import delete
from sqlalchemy.orm import sessionmaker
from base_donnees.etudiant import etudiants
from modeles_carte import modele_droit, modele_fase,modele_fasi,modele_med
Session= sessionmaker(bind=engine)
session= Session()
conceptions= session.query(preconceptions).all()
def concevoir():
    try:
        modele = 0
        requete= select(
            etudiants.c.matricule,
            preconceptions.c.id_etudiant
        ).join(etudiants, etudiants.c.id == preconceptions.c.id_etudiant)
        with engine.connect() as connection:
            resultat = connection.execute(requete)
            for row in resultat:
                if row.matricule.startswith("si"):
                    modele = modele_fasi
                elif row.matricule.startswith("ae"):
                    modele = modele_fase
                elif row.matricule.startswith("dr"):
                    modele = modele_droit
                elif row.matricule.startswith("md"):
                    modele = modele_med
                elif row.matricule.startswith("th"):
                    return f"modele pour la theologie en cours de conception"
                else:
                    print("Matricule entré invalide")
                    return None
    except Exception as e:
        print("Erreur survenue lors de la conception")
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
#                                FONCTION D'ENREGISTREMENT DANS TABLE CONCEPTION
#-------------------------------------------------------------------------------------------------------------------------
from sqlalchemy import bindparam
conception = Table('conception', metadata, autoload_with=engine, schema='public')
modeles= Table('modeles_cartes',metadata,autoload_with=engine,schema='public')
def save_conception(etudiant_id,modele_id,chemin_carte):
    try:
        if concevoir():
            insertion = conception.insert().values(
                etudiant_id= bindparam('etudiant_id'),
                modele_id= bindparam('modele_id'),
                chemin_carte= bindparam('chemin_carte')
            )
            data= {
                "etudiant_id" : preconceptions.c.id_etudiant,
                "modele_id" : modeles.c.id,
                "chemin_carte": modeles.c.chemin_modele
            }

            with engine.connect() as connection:
                connection.execute(insertion,data)
                connection.commit()
            vider_preconception()
            return True
        else:
            print("Aucune conception jusque là")
            return False
    except Exception as e: 
        print("Erreur survenue lors de l'enregistrement")

