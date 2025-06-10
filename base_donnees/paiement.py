from sqlalchemy import create_engine, MetaData, Table, bindparam, insert
# Connexion à la base de données
engine= create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
connection= engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)
# Accès à la table paiements
paiements= Table('paiements', metadata, autoload_with=engine, schema='public')
#--------------------------------------------------------------------------------------------------------------------
# Fonction enregistrement des paiements
#-------------------------------------------------------------------------------------------------------------------
def enregistrer_paiement(id_etudiant, montant):
    try:
        insertion= paiements.insert().values(
           id_etudiant= bindparam('id_etudiant'),
           montant= bindparam('montant'),
        )
        data= {
            "id_etudiant": id_etudiant,
            "montant": montant,
        }

        with engine.connect() as connection:
            connection.execute(insertion, data)
            connection.commit()
            print("Paiement enregistré avec succes!")
        
    except Exception as e :
        print("Erreur lors de l'enregistrement: ",e)