from sqlalchemy import create_engine, MetaData, Table,  insert
from sqlalchemy.exc import SQLAlchemyError
# Connexion à la base de données
engine= create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
connection= engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)
# Accès à la table paiements
paiements= Table('paiements', metadata, autoload_with=engine, schema='public')
#---------------------------------------------------------------------------------------------------------------------
# FIXATION DU MAXIMUM DE DE PAIEMENTS PAR ETUDIANT SELON LA FACULTE
#----------------------------------------------------------------------------------------------------------------------
def frais_maximal(matricule):
    prefixe= matricule[:2].lower()
    if prefixe == "si":
        return 970
    elif prefixe in ["ae","th","dr"]:
        return 915
    elif prefixe == "md":
        return 965
    else: 
        raise ValueError("Matricule entré non valide")

#--------------------------------------------------------------------------------------------------------------------
#                       Fonction enregistrement des paiements
#-------------------------------------------------------------------------------------------------------------------
from sqlalchemy import func
def save_paiement(id_etudiant,matricule, montant):
    try:
        plafond= frais_maximal(matricule)
        with engine.connect() as connection:
            total= connection.execute(
                func.sum(paiements.c.montant).select().where(paiements.c.id_etudiant == id_etudiant).scalar() or 0
            )
            frais = total + montant
            if frais> plafond:
                print("Paiement refuse! Vous etes deja en ordre")
                return
            else:
                reste= plafond - frais
                insertion= paiements.insert().values(
                id_etudiant= id_etudiant,
                montant = montant
                )
                connection.execute(insertion)
                connection.commit()
                print(f"Paiement enregistré avec succes! Il vous reste : {reste}$ a completer")
        
    except SQLAlchemyError as e :
        print("Erreur lors de l'enregistrement: ",e)

    