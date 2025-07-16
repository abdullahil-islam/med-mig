# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MdionicsZoneMapping(models.Model):
    _name = 'employee.zone.map'

    crm_team_id = fields.Many2one('crm.team')
    user_id = fields.Many2one('res.users')
    sub_city_ids = fields.Many2many('res.sub.city')
    city_ids = fields.Many2many('res.city', compute='compute_city_state_country')
    state_ids = fields.Many2many('res.country.state', compute='compute_city_state_country')
    country_ids = fields.Many2many('res.country', compute='compute_city_state_country')

    @api.depends('sub_city_ids')
    def compute_city_state_country(self):
        for rec in self:
            # city_ids = rec.sub_city_ids.city_id
            # state_ids = rec.sub_city_ids.state_id
            # country_ids = rec.sub_city_ids.country_id
            rec.city_ids.unlink()
            rec.state_ids.unlink()
            rec.country_ids.unlink()
            rec.city_ids = [(4, item.city_id.id, 0) for item in rec.sub_city_ids]
            rec.state_ids = [(4, item.state_id.id, 0) for item in rec.sub_city_ids]
            rec.country_ids = [(4, item.country_id.id, 0) for item in rec.sub_city_ids]

    def show_zone_analysis(self):
        """Action to open Zone Analysis Wizard"""
        val = {
            'crm_team_id': self.crm_team_id.id,
            'user_id': self.user_id.id,
            'name': 'Zone Mapping Analysis - {}'.format(self.env.user.name)
        }
        opportunity_counts, total, total_nill = self._compute_opportunity_counts()
        val['zone_analysis_ids'] = [(0, 0, line) for line in opportunity_counts]
        val['total'] = total
        val['total_nill'] = total_nill
        wizard = self.env['crm.zone.analysis.wizard'].create(val)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Zone Analysis',
            'res_model': 'crm.zone.analysis.wizard',
            'view_mode': 'form',
            'target': 'current',
            'res_id': wizard.id,  # Pass current record ID
        }

    def _compute_opportunity_counts(self):
        """Compute the number of opportunities per city for the given user."""
        result = []
        crm_leads = self.env['crm.lead'].search([('user_id', '=', self.user_id.id), ('type','=','opportunity')])
        total_nill = 0
        for sub_city in self.sub_city_ids:
            zone_crm = crm_leads.filtered(lambda lead: lead.sub_city_id.id == sub_city.id)
            if len(zone_crm.ids) <= 0:
                total_nill += 1
            result.append({
                'sub_city': sub_city.name,
                'crm_stage_id': [(6, 0, [crm.stage_id.id for crm in zone_crm])],
                'tag_ids': [(6, 0, [tag.id for crm in zone_crm for tag in crm.tag_ids])],
                'opportunity_count': len(zone_crm.ids),
            })
        zone_crm = crm_leads.filtered(lambda lead: not lead.sub_city_id)
        result.append({
            'sub_city': 'Unknown',
            'crm_stage_id': [(6, 0, [crm.stage_id.id for crm in zone_crm])],
            'tag_ids': [(6, 0, [tag.id for crm in zone_crm for tag in crm.tag_ids])],
            'opportunity_count': len(zone_crm.ids),
        })
        return result, len(crm_leads.ids), total_nill
