# contact.py
from odoo import api, fields, models


class ContactCategory(models.Model):
    _name = "mon_module.contact.category"
    _description = "Catégorie de contact"

    name = fields.Char(string="Nom", required=True)
    description = fields.Text(string="Description")


class Contact(models.Model):
    _name = "mon_module.contact"
    _description = "Contact"

    name = fields.Char(string="Nom", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Téléphone")
    address = fields.Text(string="Adresse")
    category_id = fields.Many2one(
        comodel_name="mon_module.contact.category",
        string="Catégorie",
    )
    related_contact_ids = fields.Many2many(
        comodel_name="mon_module.contact",
        relation="mon_module_contact_relation_rel",
        column1="contact_id",
        column2="related_contact_id",
        string="Relations",
    )

    def action_create_contact(self, vals):
        """Creation d'un contact en utilisant un dictionnaire vals"""
        return self.create(vals)

    def action_update_contact(self, vals):
        """Mise à jour d'un contact en utilisant un dictionnaire"""
        self.write(vals)
        return self

    def action_delete_contact(self):
        """Suppression d'un contact"""
        return super().unlink()

    def action_print_contacts(self):
        """Génère un rapport PDF pour les contacts sélectionnés."""
        return self.env.ref("mon_module.action_report_contacts").report_action(self)
