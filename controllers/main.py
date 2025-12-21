# controllers/main.py
from odoo import http
from odoo.http import request, Response

import os
import json
from datetime import datetime


class ContactAPI(http.Controller):
    # Chemins fixes demandés (Windows)
    LIST_PATH = r"E:\LSI-A03\erpinta\fichier.json"
    CREATE_PATH = r"E:\LSI-A03\erpinta\fichier_create.json"

    # --------- Helpers ---------
    def _ensure_dir(self, path: str) -> None:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)

    def _save_json(self, path: str, data) -> str:
        self._ensure_dir(path)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path

    def _contacts_payload(self):
        contacts = request.env["mon_module.contact"].sudo().search([])
        return [{
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "category": c.category_id.name if c.category_id else None,
            "active": c.active,
        } for c in contacts]

    # ============================================================
    # 1) JSON-RPC (Thunder/Postman -> POST JSON-RPC)
    # ============================================================

    # Liste (JSON-RPC)
    @http.route("/api/contacts", auth="user", type="json", methods=["POST"], csrf=False)
    def get_contacts(self, **kwargs):
        result = self._contacts_payload()
        saved_path = self._save_json(self.LIST_PATH, result)
        print(f"✅ Contacts JSON saved to: {saved_path}")

        return {"saved_to": saved_path, "count": len(result), "result": result}

    # Création (JSON-RPC)
    @http.route("/api/contacts/create", auth="user", type="json", methods=["POST"], csrf=False)
    def create_contact(self, **payload):
        name = payload.get("name")
        if not name:
            return {"error": "name is required"}

        vals = {
            "name": name,
            "email": payload.get("email"),
            "phone": payload.get("phone"),
            "address": payload.get("address"),
        }

        if payload.get("category_id"):
            try:
                vals["category_id"] = int(payload["category_id"])
            except Exception:
                return {"error": "category_id must be an integer"}

        rec = request.env["mon_module.contact"].sudo().create(vals)

        result = {
            "id": rec.id,
            "name": rec.name,
            "email": rec.email,
            "phone": rec.phone,
            "category_id": rec.category_id.id if rec.category_id else None,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        saved_path = self._save_json(self.CREATE_PATH, result)
        print(f"✅ Create JSON saved to: {saved_path}")

        return {"saved_to": saved_path, "result": result}

    # ============================================================
    # 2) VRAI REST (Thunder -> GET/POST classiques)
    # ============================================================

    # GET REST classique -> retourne JSON
    @http.route("/api/contacts_http", auth="user", type="http", methods=["GET"], csrf=False)
    def get_contacts_http(self, **kwargs):
        data = self._contacts_payload()
        # Optionnel: sauvegarde aussi à chaque GET REST
        saved_path = self._save_json(self.LIST_PATH, data)
        print(f"✅ (HTTP GET) Contacts JSON saved to: {saved_path}")

        return Response(
            json.dumps({"saved_to": saved_path, "count": len(data), "result": data}, ensure_ascii=False, indent=2),
            status=200,
            headers=[("Content-Type", "application/json")],
        )

    # POST REST classique -> crée un contact à partir d'un JSON raw
    @http.route("/api/contacts_http", auth="user", type="http", methods=["POST"], csrf=False)
    def create_contact_http(self, **kwargs):
        # Lire le JSON envoyé en body (Thunder -> raw JSON)
        try:
            payload = request.jsonrequest or {}
        except Exception:
            payload = {}

        name = payload.get("name")
        if not name:
            return Response(
                json.dumps({"error": "name is required"}, ensure_ascii=False, indent=2),
                status=400,
                headers=[("Content-Type", "application/json")],
            )

        vals = {
            "name": name,
            "email": payload.get("email"),
            "phone": payload.get("phone"),
            "address": payload.get("address"),
        }

        if payload.get("category_id"):
            try:
                vals["category_id"] = int(payload["category_id"])
            except Exception:
                return Response(
                    json.dumps({"error": "category_id must be an integer"}, ensure_ascii=False, indent=2),
                    status=400,
                    headers=[("Content-Type", "application/json")],
                )

        rec = request.env["mon_module.contact"].sudo().create(vals)

        result = {
            "id": rec.id,
            "name": rec.name,
            "email": rec.email,
            "phone": rec.phone,
            "category_id": rec.category_id.id if rec.category_id else None,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        saved_path = self._save_json(self.CREATE_PATH, result)
        print(f"✅ (HTTP POST) Create JSON saved to: {saved_path}")

        return Response(
            json.dumps({"saved_to": saved_path, "result": result}, ensure_ascii=False, indent=2),
            status=201,
            headers=[("Content-Type", "application/json")],
        )
        
    @http.route("/api/contacts_http/<int:contact_id>", auth="user", type="http", methods=["GET"], csrf=False)
    def get_contact_by_id_http(self, contact_id, **kwargs):
        c = request.env["mon_module.contact"].sudo().browse(contact_id)
        if not c.exists():
            return Response(
                json.dumps({"error": "Contact not found", "id": contact_id}, ensure_ascii=False, indent=2),
                status=404,
                headers=[("Content-Type", "application/json")],
            )

        data = {
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "category": c.category_id.name if c.category_id else None,
            "active": c.active,
        }

        # Optionnel: sauvegarde dans un fichier dédié
        path = rf"E:\LSI-A03\erpinta\fichier_{contact_id}.json"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return Response(
            json.dumps({"saved_to": path, "result": data}, ensure_ascii=False, indent=2),
            status=200,
            headers=[("Content-Type", "application/json")],
        )

