from sqlalchemy import create_engine, MetaData, Table, text, select
# Connexion à la base de données
engine= create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
connection= engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)
#------------------------------------------------------------------------------------------------------------------
# Fonction du remplissage de la table preconception avec le TRIGGER
#-----------------------------------------------------------------------------------------------------------------
def preconception ():
    with engine.connect() as connection:
        connection.execute(text(""
             
        ))
