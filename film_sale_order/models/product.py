from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    med_prod_type = fields.Selection(
        selection=[
            ('film', 'Film'),
            ('regular', 'Regular'),
        ],
        string='Med Product Type',
        default='regular',
        help="Type of product being sold, either Film or Series."
    )

    def action_make_products_regular(self):
        for rec in self:
            rec.med_prod_type = 'regular'
