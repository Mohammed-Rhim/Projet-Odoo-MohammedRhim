from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError

class Incident(models.Model):
    _name = "incident.management"
    _description = "Incident"
    _inherit = ["mail.thread", "mail.activity.mixin", "portal.mixin"]
    _order = "priority desc, create_date desc"

    # Basic Information
    name = fields.Char(
        string="Référence",
        readonly=True,
        copy=False,
        default="Nouveau"
    )

    title = fields.Char(string="Titre", required=True, tracking=True)
    description = fields.Text(string="Description")

    category_id = fields.Many2one(
        "incident.category",
        string="Catégorie",
        tracking=True
    )

    priority = fields.Selection(
        [
            ("0", "Basse"),
            ("1", "Moyenne"),
            ("2", "Haute"),
            ("3", "Critique"),
        ],
        string="Priorité",
        default="1",
        tracking=True
    )

    state = fields.Selection(
        [
            ("new", "Nouveau"),
            ("progress", "En cours"),
            ("pending", "En attente"),
            ("done", "Résolu"),
            ("closed", "Fermé"),
        ],
        string="État",
        default="new",
        tracking=True
    )

    # Assignment & Team
    user_id = fields.Many2one(
        "res.users",
        string="Assigné à",
        tracking=True,
        domain="[('id', 'in', available_user_ids)]"
    )
    
    team_id = fields.Many2one(
        "incident.team",
        string="Équipe",
        tracking=True
    )
    
    available_user_ids = fields.Many2many(
        "res.users",
        compute="_compute_available_users",
        string="Utilisateurs disponibles"
    )

    # SLA Management
    sla_policy_id = fields.Many2one(
        "incident.sla",
        string="Politique SLA",
        compute="_compute_sla_policy",
        store=True
    )
    
    deadline = fields.Datetime(
        string="Échéance SLA",
        compute="_compute_deadline",
        store=True,
        tracking=True
    )
    
    sla_violated = fields.Boolean(
        string="SLA Dépassé",
        compute="_compute_sla_violated",
        store=True
    )
    
    time_to_resolve = fields.Float(
        string="Temps de résolution (heures)",
        compute="_compute_time_to_resolve",
        store=True
    )
    
    resolution_date = fields.Datetime(
        string="Date de résolution",
        readonly=True
    )

    # Solution & Knowledge Base
    solution = fields.Html(string="Solution")
    
    knowledge_article_ids = fields.Many2many(
        "incident.knowledge",
        "incident_knowledge_rel",
        "incident_id",
        "knowledge_id",
        string="Articles liés"
    )

    # Portal & Customer
    partner_id = fields.Many2one(
        "res.partner",
        string="Client",
        default=lambda self: self.env.user.partner_id
    )
    
    customer_rating = fields.Selection(
        [
            ("1", "⭐"),
            ("2", "⭐⭐"),
            ("3", "⭐⭐⭐"),
            ("4", "⭐⭐⭐⭐"),
            ("5", "⭐⭐⭐⭐⭐"),
        ],
        string="Évaluation client"
    )
    
    customer_feedback = fields.Text(string="Commentaire client")

    # Computed Fields
    color = fields.Integer(string="Couleur", compute="_compute_color")

    @api.depends('team_id', 'team_id.member_ids')
    def _compute_available_users(self):
        for incident in self:
            if incident.team_id:
                incident.available_user_ids = incident.team_id.member_ids
            else:
                incident.available_user_ids = self.env['res.users'].search([])

    @api.depends('priority', 'category_id')
    def _compute_sla_policy(self):
        for incident in self:
            domain = [('priority', '=', incident.priority), ('active', '=', True)]
            if incident.category_id:
                domain = ['|', ('category_ids', '=', False), 
                         ('category_ids', 'in', incident.category_id.ids)] + domain
            sla = self.env['incident.sla'].search(domain, limit=1)
            incident.sla_policy_id = sla

    @api.depends('create_date', 'sla_policy_id', 'sla_policy_id.deadline_hours')
    def _compute_deadline(self):
        for incident in self:
            if incident.create_date and incident.sla_policy_id:
                hours = incident.sla_policy_id.deadline_hours
                incident.deadline = incident.create_date + timedelta(hours=hours)
            else:
                incident.deadline = False

    @api.depends('deadline', 'state')
    def _compute_sla_violated(self):
        now = fields.Datetime.now()
        for incident in self:
            if incident.deadline and incident.state not in ['done', 'closed']:
                incident.sla_violated = now > incident.deadline
            else:
                incident.sla_violated = False

    @api.depends('create_date', 'resolution_date')
    def _compute_time_to_resolve(self):
        for incident in self:
            if incident.create_date and incident.resolution_date:
                delta = incident.resolution_date - incident.create_date
                incident.time_to_resolve = delta.total_seconds() / 3600
            else:
                incident.time_to_resolve = 0.0

    @api.depends('priority', 'sla_violated')
    def _compute_color(self):
        for incident in self:
            if incident.sla_violated:
                incident.color = 1  # Red
            elif incident.priority == '3':
                incident.color = 9  # Pink
            elif incident.priority == '2':
                incident.color = 3  # Orange
            else:
                incident.color = 0  # Default

    @api.model
    def create(self, vals):
        if vals.get("name", "Nouveau") == "Nouveau":
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "incident.management"
            )
        
        # Auto-assign team based on category
        if vals.get('category_id') and not vals.get('team_id'):
            category = self.env['incident.category'].browse(vals['category_id'])
            team = self.env['incident.team'].search([
                ('category_ids', 'in', category.id),
                ('active', '=', True)
            ], limit=1)
            if team:
                vals['team_id'] = team.id
                # Auto-assign user from team
                if team.member_ids and not vals.get('user_id'):
                    # Find team member with least incidents
                    min_incidents = float('inf')
                    assigned_user = None
                    for member in team.member_ids:
                        count = self.search_count([
                            ('user_id', '=', member.id),
                            ('state', 'not in', ['done', 'closed'])
                        ])
                        if count < min_incidents:
                            min_incidents = count
                            assigned_user = member
                    if assigned_user:
                        vals['user_id'] = assigned_user.id
        
        return super().create(vals)

    def write(self, vals):
        # Track resolution date
        if vals.get('state') == 'done' and self.state != 'done':
            vals['resolution_date'] = fields.Datetime.now()
        return super().write(vals)

    def action_progress(self):
        self.write({'state': 'progress'})
        if not self.user_id:
            self.user_id = self.env.user

    def action_pending(self):
        self.write({'state': 'pending'})

    def action_done(self):
        if not self.solution:
            raise UserError("Veuillez fournir une solution avant de résoudre l'incident.")
        self.write({'state': 'done'})

    def action_close(self):
        self.write({'state': 'closed'})

    def action_create_knowledge_article(self):
        self.ensure_one()
        return {
            'name': 'Créer un article',
            'type': 'ir.actions.act_window',
            'res_model': 'incident.knowledge',
            'view_mode': 'form',
            'context': {
                'default_name': self.title,
                'default_content': self.solution or self.description,
                'default_category_ids': [(6, 0, self.category_id.ids)],
                'default_incident_ids': [(6, 0, [self.id])]
            }
        }
    
    def _compute_access_url(self):
        super()._compute_access_url()
        for incident in self:
            incident.access_url = f'/my/incidents/{incident.id}'
