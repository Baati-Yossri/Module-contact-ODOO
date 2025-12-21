from odoo import models, fields

class ContactCategory(models.Model):
    _name = 'mon_module.category'
    _description = 'Catégorie de contact'
    _order = 'name'

    name = fields.Char(string='Nom de la catégorie', required=True)
    description = fields.Text(string='Description')
    color = fields.Integer(string='Couleur')  # utile pour kanban (optionnel)
    active = fields.Boolean(string='Actif', default=True)  # pour archiver au lieu de supprimer

    contact_ids = fields.One2many('mon_module.contact', 'category_id', string='Contacts')

    contact_count = fields.Integer(string="Nombre de contacts", compute="_compute_contact_count")

    def _compute_contact_count(self):
        for rec in self:
            rec.contact_count = len(rec.contact_ids)
