from odoo import fields, models, api


class ModelName(models.TransientModel):
    _inherit = 'account.payment.register'

    is_courier_available = fields.Boolean(default=False)
    courier_journal_id = fields.Many2one(
        comodel_name='account.journal',
        compute='_compute_courier_journal_id', store=True, readonly=False, precompute=True,
        domain="[('id', 'in', available_journal_ids)]")
    courier_amount = fields.Monetary(currency_field='currency_id')
    courier_payment_method_line_id = fields.Many2one('account.payment.method.line', string='Payment Method',
        readonly=True, store=True,
        compute='_compute_courier_payment_method_line_id',
        domain="[('id', 'in', available_payment_method_line_ids)]",
        help="Manual: Pay or Get paid by any method outside of Odoo.\n"
        "Payment Providers: Each payment provider has its own Payment Method. Request a transaction on/to a card thanks to a payment token saved by the partner when buying or subscribing online.\n"
        "Check: Pay bills by check and print it from Odoo.\n"
        "Batch Deposit: Collect several customer checks at once generating and submitting a batch deposit to your bank. Module account_batch_payment is necessary.\n"
        "SEPA Credit Transfer: Pay in the SEPA zone by submitting a SEPA Credit Transfer file to your bank. Module account_sepa is necessary.\n"
        "SEPA Direct Debit: Get paid in the SEPA zone thanks to a mandate your partner will have granted to you. Module account_sepa is necessary.\n")
    courier_account_id = fields.Many2one('account.account', string='Courier Account')

    @api.depends('payment_type', 'courier_journal_id')
    def _compute_courier_payment_method_line_id(self):
        for wizard in self:
            if wizard.courier_journal_id:
                available_payment_method_lines = wizard.courier_journal_id._get_available_payment_method_lines(
                    wizard.payment_type)
            else:
                available_payment_method_lines = False

            # Select the first available one by default.
            if available_payment_method_lines:
                wizard.courier_payment_method_line_id = available_payment_method_lines[0]._origin
            else:
                wizard.courier_payment_method_line_id = False

    @api.depends('available_journal_ids')
    def _compute_courier_journal_id(self):
        for wizard in self:
            if wizard.can_edit_wizard:
                batch = wizard._get_batches()[0]
                wizard.journal_id = wizard._get_batch_journal(batch)
            else:
                wizard.journal_id = self.env['account.journal'].search([
                    ('type', 'in', ('bank', 'cash')),
                    ('company_id', '=', wizard.company_id.id),
                    ('id', 'in', self.available_journal_ids.ids)
                ], limit=1)

    @api.depends('can_edit_wizard', 'source_amount', 'source_amount_currency', 'source_currency_id', 'company_id',
                 'currency_id', 'payment_date', 'courier_amount')
    def _compute_amount(self):
        return super()._compute_amount()

    @api.depends('can_edit_wizard', 'amount', 'courier_amount')
    def _compute_payment_difference(self):
        return super()._compute_payment_difference()

    @api.depends('available_journal_ids')
    def _compute_courier_journal_id(self):
        for wizard in self:
            if wizard.can_edit_wizard:
                batch = wizard._get_batches()[0]
                wizard.journal_id = wizard._get_batch_journal(batch)
            else:
                wizard.journal_id = self.env['account.journal'].search([
                    ('type', 'in', ('bank', 'cash')),
                    ('company_id', '=', wizard.company_id.id),
                    ('id', 'in', self.available_journal_ids.ids)
                ], limit=1)

    @api.depends('payment_type', 'courier_journal_id')
    def _compute_courier_payment_method_line_id(self):
        for wizard in self:
            if wizard.courier_journal_id:
                available_payment_method_lines = wizard.courier_journal_id._get_available_payment_method_lines(
                    wizard.payment_type)
            else:
                available_payment_method_lines = False

            # Select the first available one by default.
            if available_payment_method_lines:
                wizard.courier_payment_method_line_id = available_payment_method_lines[0]._origin
            else:
                wizard.courier_payment_method_line_id = False

    #no need for this function
    # def _get_total_amount_using_same_currency(self, batch_result, early_payment_discount=True):
    #     res = list(super()._get_total_amount_using_same_currency(batch_result, early_payment_discount))
    #     if self.is_courier_available and self.courier_amount:
    #         res[0] -= self.courier_amount
    #     return tuple(res)

    def _create_payment_vals_from_wizard(self, batch_result):
        result = super()._create_payment_vals_from_wizard(batch_result)
        result['is_courier'] = self.is_courier_available
        result['courier_amount'] = self.courier_amount
        result['courier_expense_account'] = self.courier_account_id.id
        result['courier_payment_method_line_id'] = self.courier_payment_method_line_id.id
        result['courier_journal_id'] = self.courier_journal_id.id

        return result

    #no need for this function now because move line is generated from payment vals
    # def _create_payments(self):
    #     self.ensure_one()
    #     batches = self._get_batches()
    #     first_batch_result = batches[0]
    #     edit_mode = self.can_edit_wizard and (len(first_batch_result['lines']) == 1 or self.group_payment)
    #     to_process = []
    #
    #     if edit_mode:
    #         payment_vals = self._create_payment_vals_from_wizard(first_batch_result)
    #         to_process.append({
    #             'create_vals': payment_vals,
    #             'to_reconcile': first_batch_result['lines'],
    #             'batch': first_batch_result,
    #         })
    #         if self.is_courier_available and self.courier_amount:
    #             courier_payment_vals = payment_vals.copy()
    #             courier_payment_vals['amount'] = self.courier_amount
    #             courier_payment_vals['journal_id'] = self.courier_journal_id.id
    #             courier_payment_vals['payment_method_line_id'] = self.courier_payment_method_line_id.id
    #             to_process.append({
    #                 'create_vals': courier_payment_vals,
    #                 'to_reconcile': first_batch_result['lines'],
    #                 'batch': first_batch_result,
    #             })
    #     else:
    #         # Don't group payments: Create one batch per move.
    #         if not self.group_payment:
    #             new_batches = []
    #             for batch_result in batches:
    #                 for line in batch_result['lines']:
    #                     new_batches.append({
    #                         **batch_result,
    #                         'payment_values': {
    #                             **batch_result['payment_values'],
    #                             'payment_type': 'inbound' if line.balance > 0 else 'outbound'
    #                         },
    #                         'lines': line,
    #                     })
    #             batches = new_batches
    #
    #         for batch_result in batches:
    #             to_process.append({
    #                 'create_vals': self._create_payment_vals_from_batch(batch_result),
    #                 'to_reconcile': batch_result['lines'],
    #                 'batch': batch_result,
    #             })
    #
    #     payments = self._init_payments(to_process, edit_mode=edit_mode)
    #     self._post_payments(to_process, edit_mode=edit_mode)
    #     self._reconcile_payments(to_process, edit_mode=edit_mode)
    #     return payments
