# AR - Demande Mat?riel Informatique


> Documentation du module de demande de mat?riel informatique.


## Vue d?ensemble

Le module permet de g?rer les demandes IT pour nouveau besoin, remplacement ou emprunt. Il associe la demande au collaborateur, ? son d?partement et ? son manager, puis la transmet au service IT pour traitement, livraison ou suivi d?emprunt.

## Utilisateurs concern?s

- Demandeur : cr?e et soumet la demande.
- Manager N+1 : approuve ou refuse.
- Traiteur IT : traite, livre ou marque l?emprunt.
- Administrateur : maintient catalogue mat?riel et traiteurs.

## Workflow m?tier

1. Nouvelle
2. Validation N+1
3. Traitement IT
4. Emprunt?
5. Livr?e
6. Refus?e

## Fonctionnement op?rationnel

- Choisir nouveau besoin, remplacement ou emprunt.
- Renseigner les dates adapt?es au type de besoin.
- Ajouter les lignes mat?riel.
- Soumettre au manager.
- Traitement par IT puis livraison ou emprunt.

## Configuration recommand?e

- Cr?er le catalogue mat?riel.
- Cr?er les personnes de traitement IT.
- V?rifier les employ?s et managers.
- Configurer groupes, record rules et acc?s.

## D?pendances Odoo

- `base`
- `hr`
- `mail`
- `web`

## Mod?les techniques

- `ar.it.demande` : Demande matériel informatique (`models/demande.py`)
- `ar.it.demande.line` : Ligne demande matériel (`models/demande.py`)
- `ar.it.documentation` : IT - Documentation (`models/documentation.py`)
- `ar.it.materiel` : Matériel informatique (`models/materiel.py`)
- `ar.it.traiteur` : Personnes qui traite (`models/traite_person.py`)

## ?tats d?tect?s dans le code

- `models/demande.py` : `new` (Nouvelle), `n1` (Validation N+1), `processing` (Traitement), `borrowed` (Emprunté), `delivered` (Livrée), `refused` (Refusée)

## Actions serveur principales

- `action_submit_n1` (`models/demande.py`)
- `action_approve_n1` (`models/demande.py`)
- `action_close_processing` (`models/demande.py`)
- `action_refuse` (`models/demande.py`)

## Fichiers charg?s par le manifest

- `security/security.xml`
- `security/record_rules.xml`
- `security/ir.model.access.csv`
- `data/mail_templates.xml`
- `views/materiel_views.xml`
- `views/traite_person_views.xml`
- `views/demande_views.xml`
- `views/documentation_views.xml`
- `views/menus.xml`

## S?curit? et droits

Le module s?appuie sur les fichiers suivants pour d?finir les groupes, r?gles d?enregistrement et droits d?acc?s :

- `security/ir.model.access.csv`
- `security/record_rules.xml`
- `security/security.xml`

## Assets et interface

- `static/src/js/demande_form_animations.js`
- `static/src/scss/demande_form.scss`

## Bonnes pratiques d?utilisation

- V?rifier que chaque utilisateur Odoo est li? au bon employ? lorsque le module d?pend de `hr.employee`.
- Tester le workflow avec un dossier de test avant utilisation en production.
- Contr?ler les groupes de s?curit? apr?s installation afin que seuls les bons r?les voient les boutons de validation.
- Garder les templates e-mail et rapports align?s avec les proc?dures internes.
- Sauvegarder la base avant toute modification structurelle du module.

## Maintenance

- Les ?volutions fonctionnelles doivent ?tre ajout?es dans les mod?les Python, les vues XML et les r?gles de s?curit? correspondantes.
- Apr?s modification des vues, mettre ? jour le module depuis Odoo ou red?marrer le serveur selon le type de changement.
- Apr?s modification des assets, vider le cache navigateur et recompiler les assets si n?cessaire.
- Toute nouvelle ?tape de workflow doit ?tre accompagn?e des droits, boutons, notifications et filtres correspondants.
