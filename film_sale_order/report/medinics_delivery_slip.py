# -*- coding: utf-8 -*-
from odoo import api, models


class StoreDeliverySlipReport(models.AbstractModel):
    _name = 'report.film_sale_order.store_report_deliveryslip'
    _description = 'Store Delivery Slip Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.picking'].browse(docids)
        invoices = dict()
        shipping_addresses = dict()
        title_partners = dict()
        master_product = dict()
        # signatory = docs.company_id.signatory_delivery_slip.name
        for doc in docs:
            invoices[str(doc.id)] = doc.sale_id.invoice_ids
            sale_order = doc.sale_id
            if sale_order:
                master_product[str(doc.id)] = sale_order.order_line.mapped('product_id').ids

            shipping_address = doc.partner_id.child_ids.filtered(lambda child: child.type == 'delivery')
            if doc.shipping_partner_id:
                shipping_address = doc.shipping_partner_id
            if not shipping_address:
                shipping_address = doc.partner_id
            shipping_addresses[str(doc.id)] = shipping_address[0]

            title_partner = doc.partner_id.child_ids.filtered(lambda child: child.title.name == 'Managing Director')
            if not title_partner:
                title_partner = doc.partner_id
            title_partners[str(doc.id)] = title_partner[0]
        return {
            'docs': docs,
            'invoices': invoices,
            'report_title': 'Store Copy',
            'shipping_addresses': shipping_addresses,
            'title_partners': title_partners,
            # 'signatory': signatory or '',
            'show_report_title': True,
            'master_product': master_product
        }


class StoreCustomerDeliverySlipReport(models.AbstractModel):
    _name = 'report.stock.report_deliveryslip'
    _description = 'Customer Delivery Slip Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.picking'].browse(docids)
        invoices = dict()
        shipping_addresses = dict()
        title_partners = dict()
        master_product = dict()
        # signatory = docs.company_id.signatory_delivery_slip.name
        for doc in docs:
            invoices[str(doc.id)] = doc.sale_id.invoice_ids
            sale_order = doc.sale_id
            if sale_order:
                master_product[str(doc.id)] = sale_order.order_line.mapped(
                    'product_id').ids

            shipping_address = doc.partner_id.child_ids.filtered(lambda child: child.type == 'delivery')
            if doc.shipping_partner_id:
                shipping_address = doc.shipping_partner_id
            if not shipping_address:
                shipping_address = doc.partner_id
            shipping_addresses[str(doc.id)] = shipping_address[0]

            title_partner = doc.partner_id.child_ids.filtered(lambda child: child.title.name == 'Managing Director')
            if not title_partner:
                title_partner = doc.partner_id
            title_partners[str(doc.id)] = title_partner[0]
        return {
            'docs': docs,
            'invoices': invoices,
            'report_title': 'Customer Copy',
            'shipping_addresses': shipping_addresses,
            'title_partners': title_partners,
            # 'signatory': signatory or '',
            'show_report_title': True,
            'master_product': master_product
        }
