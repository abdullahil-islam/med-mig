from odoo import models, fields, api, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    is_courier = fields.Boolean(string='Courier')
    courier_amount = fields.Float(string='Courier Amount')
    courier_expense_account = fields.Many2one('account.account', string='Expense Account', required=False)
    courier_journal_id = fields.Many2one(
        comodel_name='account.journal')
    courier_payment_method_line_id = fields.Many2one('account.payment.method.line', string='Payment Method',
                                                     help="Manual: Pay or Get paid by any method outside of Odoo.\n"
                                                          "Payment Providers: Each payment provider has its own Payment Method. Request a transaction on/to a card thanks to a payment token saved by the partner when buying or subscribing online.\n"
                                                          "Check: Pay bills by check and print it from Odoo.\n"
                                                          "Batch Deposit: Collect several customer checks at once generating and submitting a batch deposit to your bank. Module account_batch_payment is necessary.\n"
                                                          "SEPA Credit Transfer: Pay in the SEPA zone by submitting a SEPA Credit Transfer file to your bank. Module account_sepa is necessary.\n"
                                                          "SEPA Direct Debit: Get paid in the SEPA zone thanks to a mandate your partner will have granted to you. Module account_sepa is necessary.\n")
    courier_move_id = fields.Many2one('account.move', string='Courier Journal Entry')
    sale_order_price = fields.Float()

    # def _prepare_move_line_default_vals(self, write_off_line_vals=None):
    #     result = super()._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals)
    #
    #     if self.payment_type == 'inbound' and self.is_courier and self.courier_amount > 0.0:
    #         liquidity_line = list(filter(lambda p: p['account_id'] == self.outstanding_account_id.id, result))
    #         if liquidity_line:
    #             liquidity_line[0]['amount_currency'] -= self.courier_amount
    #             liquidity_line[0]['debit'] -= self.courier_amount
    #
    #             expense_line = {
    #             'name': 'Courier Charge - {}'.format(self.ref),
    #             'date_maturity': self.date,
    #             'amount_currency': self.courier_amount,
    #             'currency_id': self.company_id.currency_id.id,
    #             'debit': self.courier_amount,
    #             'partner_id': self.partner_id.id,
    #             'account_id': self.courier_expense_account.id,
    #             }
    #             result += [expense_line]
    #
    #     return result

    def action_post(self):
        result = super().action_post()
        if self.payment_type == 'inbound' and self.is_courier and self.courier_amount > 0.0:
            courier_move = self.env['account.move'].sudo().create({
                'move_type': 'entry',
                'ref': 'Courier Charge - ' + self.ref,
                'journal_id': self.courier_journal_id.id,
                'line_ids': [(0, 0, {
                    'name': 'Courier Charge - {}'.format(self.ref),
                    'account_id': self.courier_journal_id.default_account_id.id,
                    'credit': self.courier_amount,
                    'debit': 0,
                }), (0, 0, {
                    'name': 'Courier Charge - {}'.format(self.ref),
                    'account_id': self.courier_expense_account.id,
                    'debit': self.courier_amount,
                    'credit': 0,
                })],
            })
            self.courier_move_id = courier_move.id
            courier_move.action_post()

        return result
