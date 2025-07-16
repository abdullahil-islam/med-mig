# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PaymentTerms(models.Model):
    _inherit = 'account.payment.term'

    is_full_payment = fields.Boolean(default=False)
    term_type = fields.Selection([
        ('full', 'Full Payment'),
        ('installment', 'Installment'),
        ('cash_credit', 'Cash With Credit'),
    ], default='installment', requried=True)
