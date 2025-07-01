from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Connexion à la base de données
engine = create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")
#-------------------------------------------------------------------------------------------------------------
#                       LE TRIGGER PAR LEQUEL EST REMPLI LA TABLE PRECONCEPTION
#--------------------------------------------------------------------------------------------------------------
def creer_trigger_preconception():
    try:
        script = """
        -- Supprimer d'abord l'ancien trigger et sa fonction
        DROP TRIGGER IF EXISTS trg_preconception ON paiements;
        DROP FUNCTION IF EXISTS verification_preconception;

        -- Créer la fonction de vérification pour la préconception
        CREATE OR REPLACE FUNCTION verification_preconception()
        RETURNS TRIGGER AS $$
        DECLARE
            total_paye NUMERIC := 0;
            plafond NUMERIC := 0;
            promo_etudiant TEXT;
            existe BOOLEAN;
        BEGIN
            -- Récupérer la promotion depuis la table étudiants
            SELECT promotion INTO promo_etudiant
            FROM etudiants
            WHERE id = NEW.id_etudiant;

            IF promo_etudiant IS NULL THEN
                RAISE NOTICE '⛔ Étudiant introuvable.';
                RETURN NULL;
            END IF;

            -- Nettoyage de la promotion
            promo_etudiant := LOWER(REPLACE(promo_etudiant, ' ', ''));

            -- Déterminer le plafond selon la promotion
            IF promo_etudiant = 'l1lmdfasi' THEN
                plafond := 970;
            ELSIF promo_etudiant IN ('l1lmdfase', 'l1lmddroit', 'l1lmdtheologie') THEN
                plafond := 915;
            ELSIF promo_etudiant = 'g0medecine' THEN
                plafond := 965;
            ELSE
                RAISE NOTICE '⛔ Promotion non reconnue : %', promo_etudiant;
                RETURN NULL;
            END IF;

            -- Calcul du total payé par l’étudiant
            SELECT COALESCE(SUM(montant), 0) INTO total_paye
            FROM paiements
            WHERE id_etudiant = NEW.id_etudiant;

            -- Vérifier s’il est déjà dans la table preconception
            SELECT EXISTS (
                SELECT 1 FROM preconception WHERE id_etudiant = NEW.id_etudiant
            ) INTO existe;

            -- Si le montant exact est atteint et pas encore dans preconception
            IF total_paye = plafond AND NOT existe THEN
                INSERT INTO preconception(id_etudiant, statut)
                VALUES (NEW.id_etudiant, 'en attente');
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        -- Création du trigger
        CREATE TRIGGER trg_preconception
        AFTER INSERT ON paiements
        FOR EACH ROW
        EXECUTE FUNCTION verification_preconception();
        """

        with engine.connect() as connection:
            connection.execute(text(script))
            connection.commit()
            print("✅ Trigger créé avec succès.")

    except SQLAlchemyError as e:
        print("❌ Erreur lors de la création du trigger :", e)

#    Après son exécution, la fonction n'a plus besoin d'être appelée 
#-------------------------------------------------------------------------------------------------------------
#creer_trigger_preconception()