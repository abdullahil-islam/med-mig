# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare

class AccountInvoiceCustom(models.Model):
    _inherit = "account.move"

    sale_order_id = fields.Many2one('sale.order', string="Sale Order for this Cheque")
    downpayment = fields.Float(related='sale_order_id.downpayment', string='DownPayment')
    token_money = fields.Float(related='sale_order_id.token_money', string="Booking/Token Money")
    payment_type = fields.Selection(related='sale_order_id.payment_type', string='Payment Type')
    payment_mode = fields.Selection(related='sale_order_id.payment_mode', string='Payment Mode')
    cheque_detail_ids = fields.One2many(related='sale_order_id.cheque_detail_ids', string="Cheque Details")
    downpayment_status = fields.Selection(related="sale_order_id.downpayment_status", string='DownPayment Status')
    token_money_status = fields.Selection(related="sale_order_id.token_money_status", string='Token Money Status')

    def action_register_payment(self):
        res = super(AccountInvoiceCustom, self).action_register_payment()
        res['context']['default_sale_order_id'] = self.sale_order_id.id
        return res


class AccountPaymentRegisterCustom(models.TransientModel):
    _inherit = "account.payment.register"

    sale_order_id = fields.Many2one('sale.order', string="Sale Order for this Cheque")
    cheque_detail_ids = fields.One2many(related='sale_order_id.cheque_detail_ids', string="Cheque Details")
    is_check_payment = fields.Boolean(related='journal_id.is_check_payment', string='Check Payment')
    check_id = fields.Many2one('cheque.detail')
    downpayment = fields.Float(related='sale_order_id.downpayment', string='DownPayment')
    token_money = fields.Float(related='sale_order_id.token_money', string="Booking/Token Money")
    payment_for = fields.Selection([('downpayment', 'Downpayment'), ('token', 'Token Money')],
                                   string='Payment For')
    downpayment_status = fields.Selection(related="sale_order_id.downpayment_status", string='DownPayment Status')
    token_money_status = fields.Selection(related="sale_order_id.token_money_status", string='Token Money Status')

    # @api.model
    # def default_get(self, fields):
    #     rec = super(AccountPaymentRegisterCustom, self).default_get(fields)
    #     invoice_defaults = self.resolve_2many_commands('invoice_ids', rec.get('invoice_ids'))
    #     if invoice_defaults and len(invoice_defaults) == 1:
    #         invoice = invoice_defaults[0]
    #         rec['sale_order_id'] = invoice['sale_order_id'] if invoice.get('sale_order_id') else False
    #
    #     return rec

    def action_create_payments(self):
        if self.is_check_payment and self.check_id:
            if self.amount != self.check_id.amount:
                raise ValidationError("Cheque amount and payment amount must be equal.")
            self.check_id.cheque_status = 'owner'
        return super(AccountPaymentRegisterCustom, self).action_create_payments()

class AccountPaymentCustom(models.Model):
    _inherit = "account.payment"

    sale_order_id = fields.Many2one('sale.order', string="Sale Order for this Cheque")
    cheque_detail_ids = fields.One2many(related='sale_order_id.cheque_detail_ids', string="Cheque Details")
    is_check_payment = fields.Boolean(related='journal_id.is_check_payment', string='Check Payment')
    check_id = fields.Many2one('cheque.detail')
    downpayment = fields.Float(related='sale_order_id.downpayment', string='DownPayment')
    token_money = fields.Float(related='sale_order_id.token_money', string="Booking/Token Money")
    payment_for = fields.Selection([('downpayment', 'Downpayment'), ('token', 'Token Money')],
                                   string='Payment For')
    downpayment_status = fields.Selection(related="sale_order_id.downpayment_status", string='DownPayment Status')
    token_money_status = fields.Selection(related="sale_order_id.token_money_status", string='Token Money Status')

    def post(self):
        res = super(AccountPaymentCustom, self).post()
        for rec in self:
            if rec.state == 'posted' and rec.partner_type == 'customer' and rec.sale_order_id and rec.payment_for:
                if rec.payment_for == 'token' and rec.amount == rec.token_money:
                    rec.sale_order_id.token_money_status = 'paid'
                if rec.payment_for == 'downpayment' and rec.amount == rec.downpayment:
                    rec.sale_order_id.downpayment_status = 'paid'
        return res

    def action_validate_invoice_payment(self):
        if self.is_check_payment and self.check_id:
            if self.amount != self.check_id.amount:
                raise ValidationError("Cheque amount and payment amount must be equal.")
            self.check_id.cheque_status = 'owner'
        res = super(AccountPaymentCustom, self).action_validate_invoice_payment()
        return res
