# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_equipment = fields.Boolean('Is Equipment Product')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # is_equipment = fields.Boolean('Is Equipment Product')
    equipment_id = fields.Many2one('maintenance.equipment', 'Equipment')

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        context = self._context
        if context and context.get('based_on_partner', False):
            equipment_ids = self.env['maintenance.equipment'].sudo().search(
                [('partner_id', '=', context.get('based_on_partner'))])
            product_ids = []
            for equipment in equipment_ids.filtered(lambda x: x.product_id):
                product_ids.append(equipment.product_id.id)
            args += [('id', 'in', product_ids)]
        return super(ProductProduct, self).name_search(
            name=name, args=args, operator=operator, limit=limit)