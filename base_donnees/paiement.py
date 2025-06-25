from sqlalchemy import create_engine, MetaData, Table,  insert, select
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
        return float(970)
    elif prefixe in ["ae","th","dr"]:
        return float(915)
    elif prefixe == "md":
        return float(965)
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
            requete= select(func.sum(paiements.c.montant)).where(paiements.c.id_etudiant == id_etudiant)
            total= connection.execute(requete).scalar() or 0
            frais = float(total) + montant
            if frais> plafond:
                return f"⛔ Vous avez déjà atteint le montant requis."
            insertion= paiements.insert().values(
                id_etudiant= id_etudiant,
                montant = montant
                )
            connection.execute(insertion)
            connection.commit()
            if frais == plafond:
                return f"💯 Montant requis atteint! Vous êtes à présent elligible à une carte"
            else:
                reste= float(plafond - frais)
                return f"✅ Paiement enregistré avec succès! Il vous reste : {reste}$ à completer"
        
    except SQLAlchemyError as e :
        print("Erreur lors de l'enregistrement: ",e)

    