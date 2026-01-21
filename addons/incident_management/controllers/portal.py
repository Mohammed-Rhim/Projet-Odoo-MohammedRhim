from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class IncidentPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'incident_count' in counters:
            incident_count = request.env['incident.management'].search_count([
                ('partner_id', '=', request.env.user.partner_id.id)
            ])
            values['incident_count'] = incident_count
        return values

    @http.route(['/my/incidents', '/my/incidents/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_incidents(self, page=1, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        Incident = request.env['incident.management']

        domain = [('partner_id', '=', request.env.user.partner_id.id)]

        # Filtres
        searchbar_filters = {
            'all': {'label': 'Tous', 'domain': []},
            'new': {'label': 'Nouveaux', 'domain': [('state', '=', 'new')]},
            'progress': {'label': 'En cours', 'domain': [('state', '=', 'progress')]},
            'done': {'label': 'Résolus', 'domain': [('state', '=', 'done')]},
        }

        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        # Tri
        searchbar_sortings = {
            'date': {'label': 'Date', 'order': 'create_date desc'},
            'name': {'label': 'Référence', 'order': 'name'},
            'priority': {'label': 'Priorité', 'order': 'priority desc'},
        }

        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # Pagination
        incident_count = Incident.search_count(domain)
        pager = portal_pager(
            url="/my/incidents",
            url_args={'sortby': sortby, 'filterby': filterby},
            total=incident_count,
            page=page,
            step=self._items_per_page
        )

        incidents = Incident.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'incidents': incidents,
            'page_name': 'incident',
            'pager': pager,
            'default_url': '/my/incidents',
            'searchbar_sortings': searchbar_sortings,
            'searchbar_filters': searchbar_filters,
            'sortby': sortby,
            'filterby': filterby,
        })
        return request.render("incident_management.portal_my_incidents", values)

    @http.route(['/my/incidents/<int:incident_id>'], type='http', auth="user", website=True)
    def portal_my_incident(self, incident_id, **kw):
        incident = request.env['incident.management'].browse(incident_id)
        
        # Vérifier que l'utilisateur a accès à cet incident
        if incident.partner_id != request.env.user.partner_id:
            return request.redirect('/my')

        values = {
            'incident': incident,
            'page_name': 'incident',
        }
        return request.render("incident_management.portal_my_incident", values)

    @http.route(['/my/incidents/<int:incident_id>/rate'], type='http', auth="user", website=True, methods=['POST'], csrf=True)
    def portal_incident_rate(self, incident_id, rating=None, feedback=None, **kw):
        incident = request.env['incident.management'].browse(incident_id)
        
        # Vérifier que l'utilisateur a accès à cet incident
        if incident.partner_id != request.env.user.partner_id:
            return request.redirect('/my')

        if rating:
            incident.sudo().write({
                'customer_rating': rating,
                'customer_feedback': feedback or '',
            })

        return request.redirect(f'/my/incidents/{incident_id}')
