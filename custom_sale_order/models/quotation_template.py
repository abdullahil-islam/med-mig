# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.test_impex.models import field


class QuotationTemplate(models.Model):
    _inherit = 'sale.order.template'

    cash_price = fields.Float()
    policy_price = fields.Float()
    down_payment = fields.Float()
    no_of_installment = fields.Integer()
    warranty = fields.Integer()
    ups = fields.Char()
    transportation = fields.Char()
    any_other = fields.Char()
    warranty_condition = fields.Text()

    credit_cash_price = fields.Float()
    credit_down_payment = fields.Float()
    credit_no_of_installment = fields.Integer()
    credit_warranty = fields.Integer()
    credit_ups = fields.Char()
    credit_transportation = fields.Char()
    credit_warranty_condition = fields.Text()


class QuotationTemplateLine(models.Model):
    _inherit = 'sale.order.template.line'

    is_master_product = fields.Boolean(default=False)

    def _prepare_order_line_values(self):
        res = super(QuotationTemplateLine, self)._prepare_order_line_values()
        res.update({
            'quotation_template_id': self.sale_order_template_id.id,
            'quotation_template_line_id': self.id,
            'is_master_product': self.is_master_product,
        })
        return res
