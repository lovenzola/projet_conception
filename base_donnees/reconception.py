from sqlalchemy import create_engine, MetaData, Table, select, func
from sqlalchemy.exc import SQLAlchemyError
# Connexion à la base de données
engine= create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
connection= engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)
#----------------------------------------------------------------------------------------------------------------------
#               FONCTION DE RECONCEPTION 
#----------------------------------------------------------------------------------------------------------------------
#def reconcevoir():

#-----------------------------------------------------------------------------------------------------------------------
#               FONCTION DE VERIFICATION DE CONCEPTION
#----------------------------------------------------------------------------------------------------------------------
reconception = Table('reconception',metadata,autoload_with=engine, schema='public')
def verification_reconception(etudiant_id):
    try:
        comptage= select(func.count()).where(reconception.c.etudiant_id == etudiant_id)
        with engine.connect() as connection:
            resultat= connection.execute(comptage)
            nbre_conception= resultat.scalar()
            if nbre_conception <= 3:
                print(f"Eligible à la reconception. Tentative(s) restante(s): {3-nbre_conception}")
                return True
            else:
                print("Limite atteinte! Pas eligible")
                return False
    except SQLAlchemyError as e :
        print("Erreur survenue lors de l'execution de la requete:",e)

#-------------------------------------------------------------------------------------------------------------------------
#                         ENREGISTREMENT DANS LA TABLE RECONCEPTION
#------------------------------------------------------------------------------------------------------------------------
def save_reconception(id_etudiant):
    try:
        if verification_reconception(id_etudiant):
            insertion= reconception.insert().values(etudiant_id = id_etudiant)
            with engine.connect() as connection:
                connection.execute(insertion)
    except SQLAlchemyError as e:
        print("Erreur survenue lors de l'enregistrement: ",e)