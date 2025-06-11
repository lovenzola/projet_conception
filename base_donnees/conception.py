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
preconception = Table('preconception', metadata, autoload_with=engine, schema='public')
def verification_conception():
    try:
        comptage = select(func.count()).select_from(preconception)
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
conception = Table('conception', metadata, autoload_with=engine, schema='public')












#-------------------------------------------------------------------------------------------------------------------------
#                                FONCTION D'ENREGISTREMENT DANS TABLE CONCEPTION
#-------------------------------------------------------------------------------------------------------------------------

