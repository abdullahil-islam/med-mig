from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sub_city_id = fields.Many2one('res.sub.city')
