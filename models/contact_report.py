# -*- coding: utf-8 -*-
from odoo import api, models


class ContactReport(models.AbstractModel):
    _name = "report.mon_module.contact_report_template"
    _description = "Rapport PDF des contacts"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["mon_module.contact"].browse(docids)
        if not docs:
            docs = self.env["mon_module.contact"].search([])
        return {
            "doc_ids": docs.ids,
            "doc_model": "mon_module.contact",
            "docs": docs,
        }
