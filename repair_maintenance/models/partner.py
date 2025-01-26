# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        context = self._context
        if context and context.get('based_on_product', False):
            equipment_ids = self.env['maintenance.equipment'].sudo().search(
                [('product_id', '=', context.get('based_on_product'))])
            partner_ids = []
            for equipment in equipment_ids:
                partner_ids.append(equipment.partner_id and equipment.partner_id.id)
            args += [('id', 'in', partner_ids)]
        return super(ResPartner, self).name_search(
            name=name, args=args, operator=operator, limit=limit)
        
    eq_ids = fields.One2many('maintenance.equipment','partner_id')
    eq_count = fields.Integer(compute='_compute_eq_count', string="Machine", store=True)
    # my_cus_field = fields.Char()

    @api.depends('eq_ids')
    def _compute_eq_count(self):
        self.eq_count = len(self.eq_ids)
        
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    tag_id = fields.Many2many('res.partner.category',related="partner_id.category_id", string="Tags")
        
class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    category_id = fields.Many2many('res.partner.category',related="partner_id.category_id", string="Tags")
    
    
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
            
class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    
    
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
