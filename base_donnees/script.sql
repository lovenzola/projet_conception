/* Creation des tables */
/* TABLE ETUDIANTS*/
create table if not exists etudiants (
id serial primary key,
nom varchar(50) not null,
postnom varchar(50),
prenom varchar(50),
matricule varchar(8) unique not null,
promotion varchar(20)
)

/* TABLE PAIEMENTS*/
create table if not exists paiements(
id serial primary key,
id_etudiant int not null references etudiants(id) on delete cascade,
montant numeric(10,2) not null,
date_paiement date default current_date
)

/* MODELES CARTES */
create table if not exists modeles_cartes(
id serial primary key,
nom_modele varchar(20) not null,
chemin_modele text not null,
actif boolean default false,
date_creation timestamp default current_timestamp
)

/* TABLE CONCEPTION */
create table if not exists conception(
id serial primary key,
etudiant_id integer not null references etudiants(id) on delete cascade,
date_conception timestamp default current_timestamp,
modele_id integer references modeles_cartes(id),
chemin_carte text
)

/* TABLE RECONCEPTION*/
create table if not exists reconception(
id serial primary key,
etudiant_id integer not null references etudiants(id) on delete cascade,
date_reconception timestamp default current_timestamp
)

/* Insertion des données dans la table etudiants*/
select * from etudiants 

insert into etudiants (nom,postnom,prenom,matricule,promotion)
values('nzola','samba','love','si013724','l1 lmd fasi'),
('delohim','sulemani','eclat-gabriella','si089234','l1 lmd fasi'),
('teto','filoreto','christian','si756122','l1 lmd fasi'),
('mbuyu','ilunga','franck','si431290','l1 lmd fasi'),
('nguimbi','lolo','divine','si561908','l1 lmd fasi'),
('madidi','imunga','toussaint','si756041','l1 lmd fasi'),
('kalala','odia','princesse','si879525','l1 lmd fasi'),
('musadi','kadima','theodora','si091234','l1 lmd fasi'),
('longo','longo','ainsi','si103002','l1 lmd fasi'),
('kipaka',null,'michel','si750192','l1 lmd fasi')

insert into etudiants (nom,postnom,prenom,matricule,promotion)
values ('tshikalu','masthi','fanaim','ae324155','l1 lmd fase'),
('katende','lumbu','emmanuel',)

/* TABLE PRECONCEPTION */

/* TRIGGER DU REMPLISSAGE DE PRECONCEPTION*/
CREATE OR REPLACE FUNCTION insertion_preconception()
RETURNS TRIGGER AS $$
DECLARE
    total_paye NUMERIC;
    seuil_attendu NUMERIC;
    prefixe TEXT;
BEGIN
    -- Obtenir le matricule de l’étudiant
    SELECT matricule INTO prefixe FROM etudiants WHERE id = NEW.id_etudiant;

    -- Déterminer le seuil en fonction du préfixe
    IF prefixe LIKE 'si%' THEN
        seuil_attendu := 970;
    ELSIF prefixe LIKE 'ae%' OR prefixe LIKE 'dr%' OR prefixe LIKE 'th%' THEN
        seuil_attendu := 915;
    ELSIF prefixe LIKE 'md%' THEN
        seuil_attendu := 965;

    END IF;

    -- Calculer le total payé
    SELECT SUM(montant)
    INTO total_paye
    FROM paiements
    WHERE id_etudiant = NEW.id_etudiant;

    -- Vérifier si l'étudiant a atteint le seuil et s’il n’a pas déjà été ajouté dans conception
    IF total_paye >= seuil_attendu THEN
        IF NOT EXISTS (
            SELECT 1 FROM preconception WHERE id_etudiant = NEW.id_etudiant
        ) THEN
            INSERT INTO preconception (id_etudiant, date_conception)
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
/* VIDAGE DE LA TABLE PAIEMENTS POUR DEBUTER AVEC LE TRIGGER*/
truncate table paiements restart identity cascade

/* Ajout d'une colonne pour les images des etudiants*/
alter table etudiants
add column photo_path text

/* Insertion des images pour chaque etudiant*/
update etudiants
set photo_path = case
when sexe = 'f' then  'C:\projet\multimedia\icone_femme_black.jpg'
when sexe = 'm' then  'C:\projet\multimedia\icone_homme_black.jpg'
end
where photo_path is null 


/* Insertion des valeurs dans modeles_cartes */
insert into modeles_cartes (nom_modele,chemin_modele,actif)
values('modele_fasi','C:\projet\modeles_carte\modele_fasi.py',true),
('modele_fase','C:\projet\modeles_carte\modele_fase.py',true),
('modele_droit','C:\projet\modeles_carte\modele_droit.py',true),
('modele_medecine','C:\projet\modeles_carte\modele_med.py',true),
('modele_theologie','',false)

/* Modification du chemin après les avoir condensé en un seul fichier */

select *from modeles_cartes
update modeles_cartes
set chemin_modele = 'C:\projet\modeles_carte\modeles.py'
where actif = true
select *from conception
select *from reconception

/* Modification de la table conception ; ajout d'une colonne nom_modele et suppression de cdeux colonnes*/

alter table conception
drop column modele_id,
drop column chemin_carte
select *from reconception
alter table conception 
add column nom_modele text