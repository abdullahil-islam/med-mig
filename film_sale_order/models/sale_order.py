from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sales_tag_ids = fields.Many2many('sales.order.tag', string='Sales Tags')
    is_foc = fields.Boolean(default=False)
    ref_po_wo = fields.Char('Ref/PO/WO')
    ref_po_wo_date = fields.Date('Ref/PO/WO Date')
    partner_tag_ids = fields.Many2many('res.partner.category', 'res_partner_category_sale_order_rel', string='Partner Tags', related='partner_id.category_id')
    instruction = fields.Text()
    is_film_sale = fields.Boolean(default=False)
    med_prod_type = fields.Selection(
        selection=[
            ('film', 'Film'),
            ('regular', 'Regular'),
        ],
        string='Med Product Type',
        default='film',
        help="Type of product being sold, either Film or Series."
    )

    def consider_as_foc_sale(self):
        if not self.is_foc:
            self.make_zero_so()
            self.is_foc = True
        else:
            raise ValidationError('This sale order is already considered as FOC.')

    def make_zero_so(self):
        for line in self.order_line:
            line.price_unit = 0
