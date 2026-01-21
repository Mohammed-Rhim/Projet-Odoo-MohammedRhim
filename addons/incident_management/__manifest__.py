{
    "name": "Gestion des Incidents",
    "version": "2.0",
    "summary": "Application complète de gestion des incidents IT avec SLA, équipes, base de connaissances et portail",
    "description": """
        Module Odoo 17 pour la gestion complète des incidents
        ========================================================
        
        Fonctionnalités:
        - Gestion des incidents avec workflow complet
        - SLA automatique avec alertes de dépassement
        - Équipes de support et affectation automatique
        - Base de connaissances pour solutions réutilisables
        - Portail client pour suivi et évaluation
        - Tableau de bord et analyses avancées
    """,
    "author": "Projet TP Odoo",
    "category": "Services",
    "depends": ["base", "mail", "portal"],
    "data": [
        # Sécurité
        "security/security.xml",
        "security/ir.model.access.csv",
        
        # Données
        "data/sequence.xml",
        "data/sla_data.xml",
        
        # Vues (charger les actions AVANT le menu)
        "views/category_views.xml",
        "views/sla_views.xml",
        "views/team_views.xml",
        "views/knowledge_views.xml",
        "views/incident_views.xml",
        "views/dashboard_views.xml",
        
        # Menu (doit être chargé APRÈS les vues pour référencer les actions)
        "views/menu.xml",
        
        # Portal
        "views/portal_templates.xml",
    ],
    "demo": [
        "data/demo_data.xml",
    ],
    "assets": {
        'web.assets_backend': [
            'incident_management/static/src/css/incident_management.css',
        ],
    },
    "application": True,
    "installable": True,
    "auto_install": False,
}
