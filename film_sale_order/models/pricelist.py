from odoo import fields, models, api


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    is_foc = fields.Boolean(default=False)

    @api.model
    def create(self, values):
        # Add code here

        return super(ProductPricelist, self).create(values)
