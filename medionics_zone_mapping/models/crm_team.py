from odoo import fields, models, api
from lxml import etree


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    zone_mapping_ids = fields.One2many('employee.zone.map', 'crm_team_id')

    @api.model
    def create(self, vals):
        team = super(CrmTeam, self).create(vals)
        if 'member_ids' in vals:
            team._update_zone_mappings()
        return team

    def write(self, vals):
        for team in self:
            old_members = set(team.member_ids.ids)
            res = super(CrmTeam, team).write(vals)
            if 'member_ids' in vals:
                new_members = set(team.member_ids.ids)
                added_members = new_members - old_members
                team._update_zone_mappings(added_members)
        return res

    def _update_zone_mappings(self, new_user_ids=None):
        """Creates zone mapping records for new members."""
        for team in self:
            users_to_map = self.env['res.users'].browse(new_user_ids) if new_user_ids else team.member_ids
            for user in users_to_map:
                # Check if a mapping already exists
                existing_mapping = self.env['employee.zone.map'].sudo().search([
                    ('crm_team_id', '=', team.id),
                    ('user_id', '=', user.id)
                ])
                if not existing_mapping:
                    self.env['employee.zone.map'].sudo().create({
                        'crm_team_id': team.id,
                        'user_id': user.id,
                    })


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    allowed_sub_city_ids = fields.Many2many('res.sub.city', 'crm_allowed_sub_city_red', compute='compute_allowed_address_fields', store=True)
    allowed_city_ids = fields.Many2many('res.city', 'crm_allowed_city_red', compute='compute_allowed_address_fields', store=True)
    allowed_state_ids = fields.Many2many('res.country.state', 'crm_allowed_state_red', compute='compute_allowed_address_fields', store=True)
    allowed_country_ids = fields.Many2many('res.country', 'crm_allowed_country_red', compute='compute_allowed_address_fields', store=True)

    @api.depends('team_id', 'team_id.zone_mapping_ids', 'team_id.zone_mapping_ids.sub_city_ids')
    def compute_allowed_address_fields(self):
        for rec in self:
            rec.allowed_sub_city_ids = [(5, 0, 0)]
            rec.allowed_city_ids = [(5, 0, 0)]
            rec.allowed_state_ids = [(5, 0, 0)]
            rec.allowed_country_ids = [(5, 0, 0)]
            if rec.team_id:
                zone_map = rec.team_id.zone_mapping_ids.filtered(lambda mapping: mapping.user_id.id == self.env.user.id)
                if zone_map:
                    rec.allowed_sub_city_ids = zone_map.sub_city_ids
                    rec.allowed_city_ids = zone_map.city_ids
                    rec.allowed_state_ids = zone_map.state_ids
                    rec.allowed_country_ids = zone_map.country_ids

    @api.onchange('country_id', 'state_id', 'city_id')
    def _onchange_sub_city_domain(self):
        res = super(CrmLead, self)._onchange_sub_city_domain()
        domain = res['domain']['sub_city_id']
        return {'domain': {'sub_city_id': domain + [('id', 'in', self.allowed_sub_city_ids.ids)]}}

    @api.onchange('country_id', 'state_id')
    def _onchange_city_domain(self):
        res = super(CrmLead, self)._onchange_city_domain()
        domain = res['domain']['city_id']
        return {'domain': {'city_id': domain + [('id', 'in', self.allowed_city_ids.ids)]}}

    @api.onchange('country_id')
    def _onchange_state_domain(self):
        res = super(CrmLead, self)._onchange_state_domain()
        domain = res['domain']['state_id']
        return {'domain': {'state_id': domain + [('id', 'in', self.allowed_state_ids.ids)]}}
