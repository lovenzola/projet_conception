# 1ere fonctionnalité: Enregistrer des etudiants
from sqlalchemy import create_engine, MetaData, Table, insert, select, update
from datetime import date 
from sqlalchemy.exc import SQLAlchemyError
# Connexion à la base de données
engine= create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
connection= engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)

# Accès aux tables  etudiants, conception
etudiants= Table('etudiants', metadata, autoload_with=engine, schema='public')
conception = Table('conception', metadata, autoload_with=engine, schema='public')
#-------------------------------------------------------------------------------------------------------------------
#                   Fonction enregistrement des etudiants
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
            print(f"Etudiant {nom} enregistré avec succès")
    except SQLAlchemyError as e :
        print("Erreur lors de l'enregistrement: ",e)

#---------------------------------------------------------------------------------------------------------------
#                               MODIFIER UN ENREGISTREMENT
#----------------------------------------------------------------------------------------------------------------
#   Verification de l'existence de l'ID
#-------------------------------------------------------------------------------------------
def verification_existence(id_etudiant):
    requete= select(etudiants).where(etudiants.c.id == id_etudiant)
    with engine.connect() as connection:
        resultat= connection.execute(requete).first()
        return resultat is not None
#---------------------------------------------------------------------------------------------
def modifier_info(id_etudiant, champ, nouvelle_valeur):
    try:
        champ_autorises= ["nom","postnom","prenom","sexe","date_naissance","photo_path"]
        if not verification_existence(id_etudiant):
            return f"ID inexistant"
        
        if not champ in champ_autorises:
            return f"Modification non autorisée! Champ {champ} invalide!"
        
        requete = (
            update(etudiants)
            .where(etudiants.c.id == id_etudiant)
            .values(**{champ : nouvelle_valeur}))

        with engine.connect() as connection: 
            connection.execute(requete)
            connection.commit()
            return f"✅ Modification du champ {champ} pour l'ID {id_etudiant} fait avec succès et IRREVERSIBLE ⚠️"
            
    except SQLAlchemyError as e:
        return f"Erreur survenue lors de la requête : {e}" 
