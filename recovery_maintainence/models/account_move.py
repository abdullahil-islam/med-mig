# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sb_type = fields.Selection([
        ('amc', 'AMC'),
        ('call', ' On Call'),
        ('repair', 'Repair'),
    ])


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    is_from_maintenance = fields.Boolean(default=False)
    maintenance_status_line_id = fields.Many2one('maintenance.status.line')
