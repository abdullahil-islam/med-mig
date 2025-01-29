# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.base.models import decimal_precision as dp

class HrExpense(models.Model):
    _inherit='hr.expense'
    
    partner_id = fields.Many2one(
        'res.partner', 'Customer',
        index=True,
        help='Choose partner for whom the order will be invoiced and delivered. You can find a partner by its Name, TIN, Email or Internal Reference.')
    product_id = fields.Many2one('product.product', string='Product', readonly=True, states={'draft': [('readonly', False)], 'reported': [('readonly', False)], 'refused': [('readonly', False)]}, required=True,track_visibility='onchange')
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    tag_id = fields.Many2many('res.partner.category',related="partner_id.category_id", string="Tags")
    unit_amount = fields.Float("Unit Price", readonly=True, required=True, states={'draft': [('readonly', False)], 'reported': [('readonly', False)], 'refused': [('readonly', False)]}, digits=dp.get_precision('Product Price'),track_visibility='onchange')
    quantity = fields.Float(required=True, readonly=True, states={'draft': [('readonly', False)], 'reported': [('readonly', False)], 'refused': [('readonly', False)]}, digits=dp.get_precision('Product Unit of Measure'), default=1,track_visibility='onchange')
    
    
    @api.onchange('partner_id')
    def onchange_partner_address_id(self):
        # related = 'product_id.categ_id',
        if self.partner_id:
            self.street = self.partner_id.street
            self.street2 = self.partner_id.street2
            self.zip = self.partner_id.zip
            self.city = self.partner_id.city
            self.state_id = self.partner_id.state_id and self.partner_id.state_id.id or ''
            self.country_id = self.partner_id.country_id and self.partner_id.country_id.id or ''

    def write(self, vals):
        old_unit_amount = self.unit_amount
        old_quantity = self.quantity
        res = super(HrExpense,self).write(vals)
        if self.sheet_id and vals and 'unit_amount' in vals:
            self.sheet_id.message_post(body=_("<p><strong><span class='fa fa-sun-o'></span></strong> <span>Unit Amount change by</span> <span> " + str(self.env.user.name) + "</span> <span> " + str(old_unit_amount) + "</span><span> --> </span><span> " + str(vals['unit_amount']) + "</span> </p>"))
        if self.sheet_id and vals and 'quantity' in vals:
            self.sheet_id.message_post(body=_("<p><strong><span class='fa fa-sun-o'></span></strong> <span>Quantity change by</span> <span> " + str(self.env.user.name) + "</span> <span> " + str(old_quantity) + "</span><span> --> </span><span> " + str(vals['quantity']) + "</span> </p>"))
        return res
    
    
class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    @api.model
    def create(self, vals):
        res = super(ProductProduct,self).create(vals)
        if res and res.is_equipment == True:
            res.can_be_expensed = True
        return res
