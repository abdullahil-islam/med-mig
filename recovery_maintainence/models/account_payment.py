from odoo import fields, models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    bank_ref = fields.Many2one('res.partner.bank')
    cheque_ref = fields.Char()
    cus_chq_bank_ref = fields.Char()
    effective_date = fields.Date()
    chq_deposit_date = fields.Date()
