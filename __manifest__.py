{
    'name': 'Mon Module de Contacts (TP4)',
    'version': '1.0',
    'summary': 'Gestion avancée des contacts (catégories, relations, PDF, sécurité, API, filtres, kanban)',
    'sequence': 1,
    'description': """
TP4 - Extension du module de contacts :
- Catégories
- Relations entre contacts
- Rapport PDF
- Sécurité (droits d'accès)
- API REST (JSON)
- Filtres + Kanban
    """,
    'author': 'Moi',
    'category': 'Contacts',
    'depends': ['base', 'web'],
    'data': [
    'security/ir.model.access.csv',
    'views/category_views.xml',
    'views/contact_search_views.xml',  # ✅ AVANT
    'views/contact_views.xml',         # ✅ après
    'reports/report_contacts.xml',
    'views/dashboard_views.xml',
],

    'application': True,
    'installable': True,
    'auto_install': False,
}
