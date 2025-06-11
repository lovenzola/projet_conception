select *from eleves
select *from paiement
create table temporelle(
id serial primary key,
matricule_et varchar references eleves(matricule),
date timestamp default current_timestamp
)
select *from temporelle
CREATE OR REPLACE FUNCTION insertion_preconception()
returns trigger as $$
DECLARE
    total_paye NUMERIC;
    seuil_attendu NUMERIC;
    prefixe TEXT;
BEGIN
    -- Obtenir le matricule de l’étudiant
    SELECT matricule INTO prefixe FROM eleves WHERE matricule = NEW.m_etudiant;

    -- Déterminer le seuil en fonction du préfixe
    IF prefixe LIKE 'SI%' THEN
        seuil_attendu := 970;
    ELSIF prefixe LIKE 'AE%' OR prefixe LIKE 'DR%' OR prefixe LIKE 'TH%' THEN
        seuil_attendu := 915;
    ELSIF prefixe LIKE 'MD%' THEN
        seuil_attendu := 965;

    END IF;

    -- Calculer le total payé
    SELECT SUM(montant)
    INTO total_paye
    FROM paiement
    WHERE m_etudiant = NEW.m_etudiant;

    -- Vérifier si l'étudiant a atteint le seuil et s’il n’a pas déjà été ajouté dans conception
    IF total_paye >= seuil_attendu THEN
        IF NOT EXISTS (
            SELECT 1 FROM temporelle WHERE matricule_et = NEW.m_etudiant
        ) THEN
            INSERT INTO temporelle (matricule_et)
            VALUES (NEW.m_etudiant);
        END IF;
    END IF;

    RETURN NEW;
END;
$$ language plpgsql;
create or replace trigger trigger_verif_conception
after insert on paiement
for each row 
execute function insertion_preconception();


select *from paiement
select *from temporelle
insert into paiement(m_etudiant,montant,date_paiement)
values('MD456',70,'2025-03-15'),
('MD456',70,'2025-03-15'),
('SI569',925,'2025-04-26'),
('DR345',915,'2024-11-29')

alter table temporelle
alter column date set default current_date



