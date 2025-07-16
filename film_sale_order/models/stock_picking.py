
from odoo import api, fields, models


class InheritStockPicking(models.Model):
    _inherit = 'stock.picking'

    ref_po_wo = fields.Char('Ref/PO/WO', trackings=True)
    ref_po_wo_date = fields.Date('Ref/PO/WO Date', tracking=True)
    add_contact_person = fields.Char(tracking=True)
    shipping_partner_id = fields.Many2one('res.partner', domain="[('parent_id', '=', partner_id)]")

    @api.model
    def create(self, values):
        res = super(InheritStockPicking, self).create(values)
        sale_order = self.env['sale.order'].search([('name', '=', res.origin)])
        if res.sale_id and res.picking_type_id.sequence_code == 'OUT':
            res.ref_po_wo = res.sale_id.ref_po_wo
            res.ref_po_wo_date = res.sale_id.ref_po_wo_date
        elif res.origin:
            sale_order = self.env['sale.order'].search([('name', '=', res.origin)])
            if sale_order:
                res.ref_po_wo = sale_order.ref_po_wo
                res.ref_po_wo_date = sale_order.ref_po_wo_date

        if not res.shipping_partner_id:
            addr = res.partner_id.address_get(['delivery'])
            res.shipping_partner_id = addr['delivery']
        return res

