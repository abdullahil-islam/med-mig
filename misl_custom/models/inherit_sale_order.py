# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_in_hand = fields.Float(related="product_id.qty_available", string="Available Qty")