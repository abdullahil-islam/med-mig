from odoo import models, fields, api


class CrmZoneAnalysisWizard(models.TransientModel):
    _name = "crm.zone.analysis.wizard"
    _description = "Zone Analysis Report"

    name = fields.Char()
    crm_team_id = fields.Many2one('crm.team', string="CRM Team")
    user_id = fields.Many2one('res.users', string="User")
    zone_analysis_ids = fields.One2many('crm.zone.analysis.line', 'wizard_id', string="Zone Analysis")
    total = fields.Integer('Total Opportunities')
    total_nill = fields.Integer('Nill Sub-City')


class CrmZoneAnalysisLine(models.TransientModel):
    """Wizard Line to Store City-wise Opportunity Count"""
    _name = "crm.zone.analysis.line"
    _description = "City-wise Opportunity Count"

    wizard_id = fields.Many2one('crm.zone.analysis.wizard', string="Wizard")
    sub_city = fields.Char(string="Sub City Name")
    opportunity_count = fields.Integer(string="Opportunities")
    crm_stage_id = fields.Many2many('crm.stage')
    tag_ids = fields.Many2many('crm.tag')

    def show_zone_opportunities(self):
        sub_city = self.env['res.sub.city'].search([('name', '=', self.sub_city)], limit=1)
        crm_leads = self.env['crm.lead'].search([
            ('user_id', '=', self.wizard_id.user_id.id),
            ('type','=','opportunity'),
            ('sub_city_id', '=', sub_city.id)
        ]).ids
        # return action
        return {
            'name': 'Pipeline',
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'domain': [('id', 'in', crm_leads)],
            'target': 'current',
            'view_mode': 'tree,kanban,form'
        }
