# -*- coding: utf-8 -*-

from odoo import api, exceptions, fields, models, _


class AccountInvoice(models.Model):
    _inherit = "account.move"
    
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    tag_id = fields.Many2many('res.partner.category',related="partner_id.category_id", string="Tags")
    
    
    @api.onchange('partner_id')
    def onchange_partner(self):
        # related = 'product_id.categ_id',
        if self.partner_id:
            self.street = self.partner_id.street
            self.street2 = self.partner_id.street2
            self.zip = self.partner_id.zip
            self.city = self.partner_id.city
            self.state_id = self.partner_id.state_id and self.partner_id.state_id.id or ''
            self.country_id = self.partner_id.country_id and self.partner_id.country_id.id or ''

    def amount_to_text(self, amount, currency='Euro'):
        '''Display amount in word.'''
        return self.currency_id.amount_to_text(amount)
