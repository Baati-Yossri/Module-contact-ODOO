from odoo import http
from odoo.http import request

class ContactAPI(http.Controller):
    @http.route('/api/contacts', type='json', auth='public', methods=['GET'], csrf=False)
    def get_contacts(self):
        try:
            contacts = request.env["mon_module.contact"].sudo().search([], limit=100)
            data = []
            for c in contacts:
                data.append({
                    "id": c.id,
                    "name": c.name,
                    "email": getattr(c, "email", False),
                    "phone": getattr(c, "phone", False),
                    "address": getattr(c, "address", False),
                })
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "error": str(e)}
        
        
        
    @http.route('/api/contacts', type='json', auth='public', methods=['POST'], csrf=False)
    def create_contact(self, **payload):
        try:
        
            if not payload.get("name"):
                return {"success": False, "error": "Missing required field: name"}
            elif not payload.get("email"):
                return {"success": False, "error": "Missing required field: email"}
            elif not payload.get("phone"):
                return {"success": False, "error": "Missing required field: phone"}
            
            vals = {
                "name": payload.get("name"),
                "email": payload.get("email"),
                "phone": payload.get("phone"),
                "address": payload.get("address"),
            }
            contact = request.env["mon_module.contact"].sudo().create(vals)
            return {
                "success": True,
                "data": {
                    "id": contact.id,
                    "name": contact.name,
                    "email": contact.email,
                    "phone": contact.phone,
                    "address": contact.address,
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
