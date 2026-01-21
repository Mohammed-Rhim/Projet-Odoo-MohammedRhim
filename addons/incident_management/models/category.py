from odoo import models, fields

class IncidentCategory(models.Model):
    _name = "incident.category"
    _description = "Catégorie d’incident"

    name = fields.Char(string="Nom", required=True)
    description = fields.Text(string="Description")
    color = fields.Integer(string='Couleur', default=0)
