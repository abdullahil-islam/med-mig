# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare
from datetime import datetime
from datetime import timedelta

class ChequeDetail(models.Model):
	_name = "cheque.detail"
	_description = "Cheque Detail"
	_rec_name = "cheque_number"

	sale_id = fields.Many2one('sale.order', string="Sale Order for this Cheque", required=True)
	currency_id = fields.Many2one(related='sale_id.currency_id', string="Currency")
	
	bank_id = fields.Many2one('bank.detail', string="Bank Name of this Cheque.", required=True)
	cheque_number = fields.Char(string="Cheque Number", required=True)
	cheque_date = fields.Date(string='Cheque Date', required=True)
	amount = fields.Monetary(string='Payment Amount', required=True)
	description = fields.Char(string="Description")
	cheque_status = fields.Selection([('pending', 'Pending'),
									 ('owner', 'Owner'),], string='Cheque Status', readonly=True, default="pending")
	cheque_file = fields.Binary('Cheque File', required=True)
	
	
	_sql_constraints = [
        ('cheque_uniq', 'unique(cheque_number)', 'Cheque Number must be unique per Cheque!'),
    ]

	def write(self, vals):
		res = super(ChequeDetail,self).write(vals)
		return res


class BankDetail(models.Model):
	_name = "bank.detail"
	_description = "Bank Detail"

	name = fields.Char(string="Bank Name")
	
	
class AccountJournal(models.Model):
	_inherit= 'account.journal'
	
	is_check_payment = fields.Boolean('Check Payment')


class pendingcheque(models.Model):
	_name = "cheque.pending"
	_description = "Pending Cheque"

	name = fields.Char("Name")

	@api.model
	def get_sales_details(self):
		sales_list = []
		template_engineer = self.env.ref('sale_payment_custom.cheque_pending_email_template', False)
		all_sale = self.env['sale.order'].search([('payment_type', '=', 'bank/cheque'),('state','=','sale')])
		for rec in all_sale:
			total = sum([res.amount for res in rec.cheque_detail_ids])
			total = total + rec.downpayment + rec.token_money
			if total != rec.amount_total:
				sales_list.append({'order': rec.name,'customer': rec.partner_id.name,
								'total': rec.amount_total, 'remaining': rec.amount_total - total})
		template_engineer.with_context(sales_list=sales_list).send_mail(self.id, force_send=True)
	

