from base_donnees.etudiant import etudiants 
from sqlalchemy import create_engine, MetaData, Table,  insert, select
from sqlalchemy.exc import SQLAlchemyError
# Connexion à la base de données
engine= create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
connection= engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)

#------------------------------------------------------------------------------------------------------------
#              FONCTION DE VERIFICATION DE L'EXISTENCE DE L'ETUDIANT AVANT LE PAIEMENT
#------------------------------------------------------------------------------------------------------------
# Accès à la table paiements
paiements= Table('paiements', metadata, autoload_with=engine, schema='public')

def etudiant_existe(id_etudiant):
    try:
        requete = select(etudiants.c.id).where(etudiants.c.id == id_etudiant)
        with engine.connect() as conn:
            return conn.execute(requete).first() is not None
    except Exception:
        return False
#---------------------------------------------------------------------------------------------------------------------
#               FIXATION DU MAXIMUM DE DE PAIEMENTS PAR ETUDIANT SELON LA FACULTE
#----------------------------------------------------------------------------------------------------------------------
def frais_maximal(promotion):
    prefixe= promotion.strip().lower()
    if prefixe == "l1lmdfasi":
        return float(970)
    elif prefixe in ["l1lmdfase","l1lmdtheologie","l1lmddroit"]:
        return float(915)
    elif prefixe == "g0medecine":
        return float(965)
    else: 
        raise ValueError("Promotion entré non valide")

#--------------------------------------------------------------------------------------------------------------------
#                       Fonction enregistrement des paiements
#-------------------------------------------------------------------------------------------------------------------
from sqlalchemy import func

def save_paiement(id_etudiant,  montant):
    try:
        with engine.connect() as connection:
            # Vérification que l'étudiant existe
            etudiants = Table('etudiants', metadata, autoload_with=engine, schema='public')
            requete_existence = select(func.count()).select_from(etudiants).where(etudiants.c.id == id_etudiant)
            existe = connection.execute(requete_existence).scalar()

            if not existe:
                return "⛔ Étudiant inexistant. Veuillez vérifier l'ID."

            # Vérification du plafond
            requete_promo= select(etudiants.c.promotion).where(etudiants.c.id == id_etudiant)
            resultat= connection.execute(requete_promo).scalar()

            promotion= resultat.strip().lower().replace(" ","")
            plafond = frais_maximal(promotion)
            requete = select(func.sum(paiements.c.montant)).where(paiements.c.id_etudiant == id_etudiant)
            total = connection.execute(requete).scalar() or 0
            frais = float(total) + montant

            if frais > plafond:
                return "⛔ Vous avez déjà atteint le montant requis."

            # Insertion du paiement
            insertion = paiements.insert().values(
                id_etudiant=id_etudiant,
                montant=montant
            )
            connection.execute(insertion)
            connection.commit()

            if frais == plafond:
                return "💯 Montant requis atteint! Vous êtes à présent éligible à une carte"
            else:
                reste = float(plafond - frais)
                return f"✅ Paiement enregistré avec succès! Il vous reste : {reste}$ à compléter"

    except SQLAlchemyError as e:
        print("Erreur lors de l'enregistrement: ", e)
        return "❌ Une erreur s'est produite lors de l'enregistrement du paiement."