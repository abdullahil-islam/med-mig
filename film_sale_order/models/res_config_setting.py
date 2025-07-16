# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons.test_impex.models import field


class ResCompany(models.Model):
    _inherit = 'res.company'

    signatory_delivery_slip = fields.Many2one('res.users', readonly=False, string='Signatory For Delivery Slip')
    signatory_invoice = fields.Many2one('res.users', readonly=False, string='Signatory For Invoice')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    signatory_delivery_slip = fields.Many2one('res.users', related='company_id.signatory_delivery_slip', readonly=False, string='Signatory For Delivery Slip')
    signatory_invoice = fields.Many2one('res.users', related='company_id.signatory_invoice', readonly=False, string='Signatory For Invoice')

