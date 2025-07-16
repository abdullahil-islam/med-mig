from odoo import fields, models, api


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    bank_ref = fields.Many2one('res.partner.bank')
    cheque_ref = fields.Char()
    cus_chq_bank_ref = fields.Char()
    effective_date = fields.Date()
    chq_deposit_date = fields.Date()

    def _create_payment_vals_from_wizard(self, batch_result):
        payment_vals = super()._create_payment_vals_from_wizard(batch_result=batch_result)
        payment_vals.update({
            'bank_ref': self.bank_ref.id,
            'cheque_ref': self.cheque_ref,
            'cus_chq_bank_ref': self.cus_chq_bank_ref,
            'effective_date': self.effective_date,
            'chq_deposit_date': self.chq_deposit_date,
        })
        return payment_vals
