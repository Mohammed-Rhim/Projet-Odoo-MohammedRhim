from odoo import models, fields, api

class KnowledgeArticle(models.Model):
    _name = "incident.knowledge"
    _description = "Article de Base de Connaissances"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, id desc"

    name = fields.Char(string="Titre", required=True, tracking=True)
    
    content = fields.Html(string="Contenu", required=True)
    
    category_ids = fields.Many2many(
        "incident.category",
        "knowledge_category_rel",
        "knowledge_id",
        "category_id",
        string="Catégories"
    )
    
    tag_ids = fields.Many2many(
        "incident.knowledge.tag",
        string="Tags",
        help="Tags pour faciliter la recherche"
    )
    
    author_id = fields.Many2one(
        "res.users",
        string="Auteur",
        default=lambda self: self.env.user,
        readonly=True
    )
    
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("published", "Publié"),
            ("archived", "Archivé"),
        ],
        string="État",
        default="draft",
        tracking=True
    )
    
    view_count = fields.Integer(string="Nombre de vues", default=0, readonly=True)
    
    helpful_count = fields.Integer(string="Votes utiles", default=0, readonly=True)
    
    sequence = fields.Integer(string="Séquence", default=10)
    
    incident_ids = fields.Many2many(
        "incident.management",
        "incident_knowledge_rel",
        "knowledge_id",
        "incident_id",
        string="Incidents liés"
    )
    
    incident_count = fields.Integer(
        string="Nombre d'incidents",
        compute="_compute_incident_count"
    )
    
    create_date = fields.Datetime(string="Date de création", readonly=True)
    write_date = fields.Datetime(string="Dernière modification", readonly=True)
    
    @api.depends('incident_ids')
    def _compute_incident_count(self):
        for article in self:
            article.incident_count = len(article.incident_ids)
    
    def action_publish(self):
        self.write({'state': 'published'})
    
    def action_archive_article(self):
        self.write({'state': 'archived'})
    
    def action_draft(self):
        self.write({'state': 'draft'})
    
    def action_increment_view(self):
        for article in self:
            article.view_count += 1
    
    def action_mark_helpful(self):
        for article in self:
            article.helpful_count += 1


class KnowledgeTag(models.Model):
    _name = "incident.knowledge.tag"
    _description = "Tag de Base de Connaissances"

    name = fields.Char(string="Nom", required=True)
    color = fields.Integer(string="Couleur", default=0)
    
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Ce tag existe déjà!')
    ]
