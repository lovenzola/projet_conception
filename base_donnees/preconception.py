from sqlalchemy import create_engine, text

# Connexion à la base de données
engine = create_engine("postgresql+psycopg2://postgres:12345678@localhost:5433/conception_carte")

def creer_trigger_preconception():
    try:
        script = """
        DROP TRIGGER IF EXISTS trigger_verif_conception ON paiements;
        DROP FUNCTION IF EXISTS insertion_preconception;

        CREATE OR REPLACE FUNCTION insertion_preconception()
        RETURNS TRIGGER AS $$
        DECLARE
            total_paye NUMERIC;
            seuil_attendu NUMERIC;
            prefixe TEXT;
        BEGIN
            SELECT matricule INTO prefixe FROM etudiants WHERE id = NEW.id_etudiant;

            IF prefixe LIKE 'si%' THEN
                seuil_attendu := 970;
            ELSIF prefixe LIKE 'ae%' OR prefixe LIKE 'dr%' OR prefixe LIKE 'th%' THEN
                seuil_attendu := 915;
            ELSIF prefixe LIKE 'md%' THEN
                seuil_attendu := 965;
            ELSE
                RETURN NEW; -- Si le matricule est inconnu, on ne fait rien
            END IF;

            SELECT SUM(montant) INTO total_paye
            FROM paiements
            WHERE id_etudiant = NEW.id_etudiant;

            IF total_paye >= seuil_attendu THEN
                IF NOT EXISTS (
                    SELECT 1 FROM preconception WHERE id_etudiant = NEW.id_etudiant
                ) THEN
                    INSERT INTO preconception (id_etudiant, date)
                    VALUES (NEW.id_etudiant, CURRENT_DATE);
                END IF;
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trigger_verif_conception
        AFTER INSERT ON paiements
        FOR EACH ROW
        EXECUTE FUNCTION insertion_preconception();
        """
        with engine.connect() as connection:
            connection.execute(text(script))
            connection.commit()
            print("✅ Trigger créé avec succès !")
    except Exception as e:
        print("❌ Erreur lors de la création du trigger:", e)

    