from odoo import models, fields, api

class SLAPolicy(models.Model):
    _name = "incident.sla"
    _description = "SLA Policy"
    _order = "priority desc"

    name = fields.Char(string="Nom de la Politique SLA", required=True)
    description = fields.Text(string="Description")
    
    priority = fields.Selection(
        [
            ("0", "Basse"),
            ("1", "Moyenne"),
            ("2", "Haute"),
            ("3", "Critique"),
        ],
        string="Priorité",
        required=True,
        help="Priorité d'incident à laquelle cette politique s'applique"
    )
    
    category_ids = fields.Many2many(
        "incident.category",
        string="Catégories",
        help="Catégories auxquelles cette politique s'applique. Laisser vide pour toutes les catégories."
    )
    
    deadline_hours = fields.Float(
        string="Délai (heures)",
        required=True,
        help="Nombre d'heures pour résoudre l'incident"
    )
    
    active = fields.Boolean(string="Actif", default=True)
    
    color = fields.Integer(string="Couleur", default=0)
    
    _sql_constraints = [
        ('unique_priority_category', 
         'unique(priority)', 
         'Une seule politique SLA par priorité est autorisée!')
    ]
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.name} ({record.deadline_hours}h)"
            result.append((record.id, name))
        return result
