from odoo import models, fields

class Contact(models.Model):
    _name = 'mon_module.contact'
    _description = 'Contact personnalisé'
    _order = 'name'

    name = fields.Char(string='Nom', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Téléphone')
    address = fields.Text(string='Adresse')
    active = fields.Boolean(default=True)

    # Étape 1 — catégorisation
    category_id = fields.Many2one(
        'mon_module.category',
        string='Catégorie',
        ondelete='set null'
    )

    # Étape 2 — relations entre contacts (self-M2M)
    related_contact_ids = fields.Many2many(
        'mon_module.contact',
        'mon_module_contact_rel',
        'src_contact_id', 'dst_contact_id',
        string='Contacts liés',
        help="Amis, collègues, etc. (sélection multiple)"
    )

    # (Optionnel) miroir pour affichage (lecture seule possible dans la vue)
    related_by_contact_ids = fields.Many2many(
        'mon_module.contact',
        'mon_module_contact_rel',
        'dst_contact_id', 'src_contact_id',
        string='Lié par'
    )

    def action_toggle_active(self):
        for rec in self:
            rec.active = not rec.active
