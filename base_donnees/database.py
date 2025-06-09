# 1ere fonctionnalité: Enregistrer des etudiants
from sqlalchemy import create_engine, MetaData, Table, bindparam, insert
from datetime import date 

# Connexion à la base de données
engine= create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
connection= engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)

# Accès à la table etudiants
etudiants= Table('etudiants', metadata, autoload_with=engine, schema='public')

# Fonction enregistrement des etudiants

def enregistrer_etudiant(nom,postnom,prenom,matricule,promotion,sexe, date_naissance):
    try:
        insertion= etudiants.insert().values(
            nom= bindparam('nom'),
            postnom= bindparam('postnom'),
            prenom= bindparam('prenom'),
            matricule= bindparam('matricule'),
            promotion= bindparam('promotion'),
            sexe= bindparam('sexe'),
            date_naissance= bindparam('date_naissance')
        )
        data= {
            "nom":nom,
            "postnom": postnom,
            "prenom": prenom,
            "matricule": matricule,
            "promotion": promotion,
            "sexe": sexe,
            "date_naissance": date_naissance
        }

        with engine.connect() as connection:
            connection.execute(insertion, data)
            connection.commit()
            print(f"Etudiant {nom} enregistré avec succes!")
        
    except Exception as e :
        print("Erreur lors de l'enregistrement: ",e)

