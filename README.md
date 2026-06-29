# AR - Demande Materiel Informatique

Module Odoo de gestion des demandes de materiel informatique.

Le module couvre les nouveaux besoins, les remplacements et les emprunts temporaires, avec validation Manager N+1 puis traitement par l'equipe IT.

## Objectif fonctionnel

Centraliser les demandes IT et tracer les validations, traitements, livraisons et emprunts.

Le module permet de :

- creer une demande de materiel informatique ;
- choisir le type de besoin ;
- saisir les dates obligatoires selon le type ;
- ajouter les lignes de materiel ;
- joindre des pieces justificatives ;
- soumettre au Manager N+1 ;
- faire valider ou refuser la demande ;
- transmettre au traitement IT ;
- marquer le materiel comme livre ou emprunte ;
- notifier les acteurs par email.

## Roles fonctionnels

### Demandeur

Le demandeur cree la demande et renseigne le besoin.

Il peut :

- creer une demande ;
- choisir `Nouveau besoin`, `Remplacement` ou `Emprunter` ;
- saisir la date de besoin, la date de remplacement ou la periode d'emprunt ;
- ajouter le materiel demande ;
- joindre des fichiers ;
- soumettre la demande ;
- suivre son avancement.

### Manager N+1

Le Manager N+1 valide ou refuse apres soumission.

Condition importante : l'utilisateur doit etre le Manager N+1 reel du demandeur.

### Traiteur IT

Le traiteur IT intervient apres validation N+1.

Il peut :

- consulter les demandes en traitement ;
- preparer le materiel ;
- cloturer en `Livree` ;
- cloturer en `Emprunte` lorsque le besoin est temporaire ;
- refuser si le traitement n'est pas possible.

### Administrateur

L'administrateur gere le catalogue materiel, les traiteurs IT, la documentation et les droits.

## Types de demande

Le champ `Expression de besoin` peut prendre les valeurs suivantes :

- `Nouveau besoin`
- `Remplacement`
- `Emprunter`

Regles de saisie :

- pour `Nouveau besoin`, la date de besoin est obligatoire ;
- pour `Remplacement`, la date de remplacement est obligatoire ;
- pour `Emprunter`, les dates `Du` et `Au` sont obligatoires ;
- la date `Au` doit etre superieure ou egale a la date `Du`.

## Etats du workflow

Les etats principaux sont :

- `Nouvelle`
- `Validation N+1`
- `Traitement`
- `Emprunte`
- `Livree`
- `Refusee`

## Flux standard

1. `Nouvelle`
2. `Validation N+1`
3. `Traitement`
4. `Livree` ou `Emprunte`

Un refus peut intervenir a l'etape Manager N+1 ou traitement IT.

## Donnees de reference

Le module utilise :

- un catalogue de materiels ;
- un referentiel des traiteurs IT ;
- une documentation interne.

## Notifications

Les templates email couvrent notamment :

- nouvelle demande vers Manager N+1 ;
- demande approuvee vers demandeur ;
- demande en traitement vers traiteurs IT ;
- demande livree vers demandeur ;
- demande empruntee vers demandeur ;
- demande refusee vers demandeur.

Fichier principal :

- `data/mail_templates.xml`

## Securite et droits

Les droits sont definis dans :

- `security/security.xml`
- `security/record_rules.xml`
- `security/ir.model.access.csv`

Points de controle :

- seul le demandeur cree et soumet sa demande ;
- seul le Manager N+1 valide l'etape N+1 ;
- seuls les traiteurs IT autorises traitent les demandes ;
- les contraintes de dates sont appliquees cote serveur.

## Modeles principaux

- `ar.it.demande`
- `ar.it.demande.line`
- `ar.it.materiel`
- `ar.it.traiteur`
- `ar.it.documentation`

## Structure du module

- `security/security.xml`
- `security/record_rules.xml`
- `security/ir.model.access.csv`
- `data/mail_templates.xml`
- `views/materiel_views.xml`
- `views/traite_person_views.xml`
- `views/demande_views.xml`
- `views/documentation_views.xml`
- `views/menus.xml`
- `models/demande.py`
- `models/materiel.py`
- `models/traite_person.py`
- `models/documentation.py`
- `static/src/scss/demande_form.scss`
- `static/src/js/demande_form_animations.js`

## Installation

1. Copier le module dans le dossier addons Odoo.
2. Redemarrer le serveur Odoo si necessaire.
3. Mettre a jour la liste des applications.
4. Installer le module.
5. Creer le catalogue materiel.
6. Declarer les traiteurs IT.
7. Verifier les managers dans les fiches employes.
8. Tester un flux `Nouveau besoin`, `Remplacement` et `Emprunter`.

## Maintenance fonctionnelle

Lorsqu'un type de demande ou une regle de date change, verifier aussi :

- les contraintes Python ;
- les champs visibles dans les vues ;
- les boutons de workflow ;
- les templates email ;
- les record rules ;
- ce README.
