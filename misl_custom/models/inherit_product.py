from odoo import models, fields, api
from odoo.osv import expression


class Product(models.Model):
    _inherit = 'product.product'

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if not args:
            args = []
        # if not self.env.context.get('search_equipment'):
        #     args += [('is_equipment', '=', False)]
        return super(Product, self)._name_search(name=name, args=args, operator=operator, limit=limit,
                                                 name_get_uid=name_get_uid)
