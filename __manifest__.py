# vues/manifest.py
{
    "name": "Gestion de Contacts",
    "summary": "Module de gestion des contacts",
    "description": "Ajout, Modification et supression des contact (ainsi que des relations entre eux).",
    "version": "1.0.0",
    "category": "Tools",
    "author": "Yosri",
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/contact_views.xml",
        "report/contact_report_templates.xml",
    ],
    "installable": True,
    "application": True,
}
