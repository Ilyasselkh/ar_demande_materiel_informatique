# AR - Demande Matériel Informatique

Module Odoo de gestion des demandes de matériel informatique.

## Objectif

Ce module permet aux collaborateurs de demander un nouveau matériel, un remplacement ou un emprunt temporaire, avec validation manager puis traitement par le service informatique.

## Dépendances

- `base`
- `hr`
- `mail`
- `web`

## Modèles principaux

- `ar.it.demande` : demande de matériel.
- `ar.it.demande.line` : lignes de matériel demandé.
- `ar.it.materiel` : catalogue matériel.
- `ar.it.traiteur` : personnes qui traitent les demandes.
- `ar.it.documentation` : documentation métier.

## Workflow

1. `new` : nouvelle demande.
2. `n1` : validation manager N+1.
3. `processing` : traitement IT.
4. `borrowed` : matériel emprunté.
5. `delivered` : matériel livré.
6. `refused` : demande refusée.

## Fonctionnement

- Le demandeur, le département et le manager sont déduits de `hr.employee`.
- Le type de besoin peut être nouveau, remplacement ou emprunt.
- Les dates obligatoires changent selon le type de besoin : date de besoin, date de remplacement ou période d'emprunt.
- Les lignes détaillent les matériels demandés.
- Le manager valide, puis l'équipe IT traite et clôture par livraison ou emprunt.
- Le chatter conserve les validations, refus et commentaires.

## Sécurité

Les groupes, règles d'enregistrement et accès sont définis dans :

- `security/security.xml`
- `security/record_rules.xml`
- `security/ir.model.access.csv`

## Interface

Le module ajoute les vues de matériel, traiteurs, demandes, documentation et menus, avec SCSS/JS backend pour améliorer l'expérience utilisateur.

