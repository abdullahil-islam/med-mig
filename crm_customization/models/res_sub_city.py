from odoo import fields, models, api


class ResSubCity(models.Model):
    _name = 'res.sub.city'
    _description = 'Res Sub Cities'

    name = fields.Char()
    city_id = fields.Many2one('res.city')
    state_id = fields.Many2one('res.country.state', related='city_id.state_id')
    country_id = fields.Many2one('res.country', related='city_id.country_id')
