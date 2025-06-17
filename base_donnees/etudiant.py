# 1ere fonctionnalité: Enregistrer des etudiants
from sqlalchemy import create_engine, MetaData, Table, insert
from datetime import date 
from sqlalchemy.exc import SQLAlchemyError
# Connexion à la base de données
engine= create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
connection= engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)

# Accès à la table etudiants
etudiants= Table('etudiants', metadata, autoload_with=engine, schema='public')
#-------------------------------------------------------------------------------------------------------------------
# Fonction enregistrement des etudiants
#-------------------------------------------------------------------------------------------------------------------
def save_etudiant(nom,postnom,prenom,matricule,promotion,sexe, date_naissance,photo_path):
    try:
        insertion= etudiants.insert().values(
            nom= nom,
            postnom= postnom,
            prenom= prenom,
            matricule= matricule,
            promotion= promotion,
            sexe = sexe,
            date_naissance= date_naissance,
            photo_path = photo_path

        )
        with engine.connect() as connection:
            connection.execute(insertion)
            connection.commit()
            print(f"Etudiant {nom} enregistré avec succes!")
        
    except SQLAlchemyError as e :
        print("Erreur lors de l'enregistrement: ",e)

