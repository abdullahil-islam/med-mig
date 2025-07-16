# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    shipping_partner_id = fields.Many2one('res.partner', domain="[('parent_id', '=', partner_id)]")

    @api.model
    def create(self, values):
        res = super(StockPicking, self).create(values)
        if not res.shipping_partner_id:
            addr = res.partner_id.address_get(['delivery'])
            res.shipping_partner_id = addr['delivery']
        # Add code here
        return res
