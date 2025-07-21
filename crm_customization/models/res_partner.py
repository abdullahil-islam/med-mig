from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sub_city_id = fields.Many2one('res.sub.city')

    @api.onchange('country_id')
    def _onchange_state_domain(self):
        domain = []
        if self.country_id:
            domain.append(('country_id', '=', self.country_id.id))
        return {'domain': {'state_id': domain}}

    @api.onchange('country_id', 'state_id')
    def _onchange_city_domain(self):
        domain = []
        if self.country_id:
            domain.append(('country_id', '=', self.country_id.id))
        if self.state_id:
            domain.append(('state_id', '=', self.state_id.id))
        return {'domain': {'city_id': domain}}

    @api.onchange('country_id', 'state_id', 'city_id')
    def _onchange_sub_city_domain(self):
        """
        Set domain for sub_city_id dynamically based on country, state and city.
        """
        domain = []
        if self.country_id:
            domain.append(('country_id', '=', self.country_id.id))
        if self.state_id:
            domain.append(('state_id', '=', self.state_id.id))
        if self.city_id:
            domain.append(('city_id', '=', self.city_id.id))
        return {'domain': {'sub_city_id': domain}}

    @api.onchange('sub_city_id')
    def onchange_sub_city_id(self):
        if self.sub_city_id:
            self.city = self.sub_city_id.city_id.name
            self.city_id = self.sub_city_id.city_id.id
            self.state_id = self.sub_city_id.state_id.id if self.sub_city_id.state_id else False
            self.country_id = self.sub_city_id.country_id.id

    @api.onchange('city_id')
    def onchange_city_id(self):
        if self.city_id:
            self.city = self.city_id.name
            self.state_id = self.city_id.state_id.id if self.city_id.state_id else False
            self.country_id = self.city_id.country_id.id
