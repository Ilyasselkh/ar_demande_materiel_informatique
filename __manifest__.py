{
    "name": "AR - Demande matériel informatique",
    "version": "1.0.0",
    "category": "Operations",
    "summary": "Gestion des demandes de matériel informatique",
    "depends": ["base", "hr", "mail", "web"],
    "data": [
    "security/security.xml",
    "security/record_rules.xml",
    "security/ir.model.access.csv",
    "data/mail_templates.xml",
    "views/materiel_views.xml",
    "views/traite_person_views.xml",
    "views/demande_views.xml",
    "views/documentation_views.xml",
    "views/menus.xml",
],
    "assets": {
        "web.assets_backend": [
            "ar_demande_materiel_informatique/static/src/scss/demande_form.scss",
            "ar_demande_materiel_informatique/static/src/js/demande_form_animations.js",
        ],
    },

    "application": True,
    "installable": True,
}
