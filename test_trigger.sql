select *from eleves
select *from paiement
create table temporelle(
id serial primary key,
matricule_et varchar references eleves(matricule),
date timestamp default current_timestamp
)
select *from temporelle
