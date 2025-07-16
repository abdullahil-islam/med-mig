# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo import Command


class SaleCustom(models.Model):
	_inherit = "sale.order"
	_description = 'Sale Order'

	payment_type = fields.Selection([('cash', 'Cash'),('bank/cheque', 'Bank/Cheque'),], string='Payment Type')
	payment_mode = fields.Selection([('cash_cheque', 'Cash Cheque'),
									 ('account_pay_cheque', 'Account Pay Cheque'),
									 ('pay_order', 'Pay Order'),
									 ('online_deposit', 'Online Deposit'),
									 ('mobile_banking', 'Mobile Banking'),], string='Payment Mode')
	downpayment = fields.Float('DownPayment')
	token_money = fields.Float("Booking/Token Money")
	cheque_detail_ids = fields.One2many('cheque.detail', 'sale_id', string="Cheque Details")
	downpayment_status = fields.Selection([('pending', 'Pending'),('Partial', 'Partial paid'),('paid', 'Paid'),], string='DownPayment Status', default="pending")
	token_money_status = fields.Selection([('pending', 'Pending'),('Partial', 'Partial paid'),('paid', 'Paid'),], string='Token Money Status', default="pending")
	
	
# 	@api.model
# 	def create(self,vals):
# 		res = super(SaleCustom,self).create(vals)
# 		if res.payment_type and res.payment_type == 'bank/cheque':
# 			total = sum([rec.amount for rec in res.cheque_detail_ids])
# 			total = total + res.downpayment
# 			if total != res.amount_total:
# 				raise ValidationError(_('Cheque payment must be same as sale amount.'))
# 		return res

	def _prepare_invoice(self):
        
		self.ensure_one()
		invoice_vals = {
			'sale_order_id': self.id,
			'narration': self.note,
			'payment_type': self.payment_type,
            'ref': self.client_order_ref or '',
			'move_type': 'out_invoice',
			'currency_id': self.currency_id.id,
			'campaign_id': self.campaign_id.id,
			'medium_id': self.medium_id.id,
			'source_id': self.source_id.id,
			'team_id': self.team_id.id,
			'partner_id': self.partner_invoice_id.id,
			'partner_shipping_id': self.partner_shipping_id.id,
			'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id._get_fiscal_position(
				self.partner_invoice_id)).id,
			'invoice_origin': self.name,
			'invoice_payment_term_id': self.payment_term_id.id,
			'invoice_user_id': self.user_id.id,
			'payment_reference': self.reference,
			'transaction_ids': [Command.set(self.transaction_ids.ids)],
			'company_id': self.company_id.id,
			'invoice_line_ids': [],
			'user_id': self.user_id.id,
        }
		print(invoice_vals)
		return invoice_vals
	
# class account_payment(models.Model):
# 	_inherit = 'account.payment'
# 	
# 	sale_order_id = fields.Many2one('sale.order', string="Sales Order")
# 	downpayment = fields.Float(related='sale_order_id.downpayment',string='DownPayment')
# 	token_money = fields.Float(related='sale_order_id.token_money',string="Booking/Token Money")
# 	payment_for = fields.Selection([('downpayment', 'Downpayment'),('token', 'Token Money'),], string='Payment For')
# 	
# 	
# 	@api.onchange('state')
# 	def onchange_state(self):
# 		for rec in self:
# 			if rec.state == 'posted' and rec.partner_type == 'customer' and rec.sale_order_id and rec.payment_for:
# 				if rec.payment_for == 'token' and rec.amount == rec.token_money:
# 					rec.sale_order_id.token_money_status = 'paid'
# 				if rec.payment_for == 'downpayment' and rec.amount == rec.downpayment:
# 					rec.sale_order_id.downpayment_status = 'paid'
# 				

