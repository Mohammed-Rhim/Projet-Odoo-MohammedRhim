from odoo import models, fields, api

class SupportTeam(models.Model):
    _name = "incident.team"
    _description = "Équipe de Support"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Nom de l'équipe", required=True, tracking=True)
    description = fields.Text(string="Description")
    
    team_leader_id = fields.Many2one(
        "res.users",
        string="Chef d'équipe",
        tracking=True
    )
    
    member_ids = fields.Many2many(
        "res.users",
        "incident_team_member_rel",
        "team_id",
        "user_id",
        string="Membres de l'équipe"
    )
    
    category_ids = fields.Many2many(
        "incident.category",
        "incident_team_category_rel",
        "team_id",
        "category_id",
        string="Spécialisations",
        help="Catégories d'incidents gérées par cette équipe"
    )
    
    active = fields.Boolean(string="Actif", default=True)
    
    incident_count = fields.Integer(
        string="Nombre d'incidents",
        compute="_compute_incident_count"
    )
    
    color = fields.Integer(string="Couleur", default=0)
    
    @api.depends('member_ids')
    def _compute_incident_count(self):
        for team in self:
            team.incident_count = self.env['incident.management'].search_count([
                ('team_id', '=', team.id),
                ('state', 'not in', ['done', 'closed'])
            ])
    
    def action_view_incidents(self):
        self.ensure_one()
        return {
            'name': f'Incidents - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'incident.management',
            'view_mode': 'tree,form',
            'domain': [('team_id', '=', self.id)],
            'context': {'default_team_id': self.id}
        }
