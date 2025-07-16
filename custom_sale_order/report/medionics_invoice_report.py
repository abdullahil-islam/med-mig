# -*- coding: utf-8 -*-

from odoo import api, fields, models
from num2words import num2words


class MedionnicsReportInvoice(models.AbstractModel):
    _name = 'report.custom_sale_order.report_medionics_invoice'
    _description = 'Medionics Account report'

    def convert_to_ordinal(self, n):
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return "{}{}".format(n, suffix)

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)
        # self.currency_id.amount_to_text(self.amount) if self.currency_id else False
        picking_names = dict()
        shipping_addresses = dict()
        title_partners = dict()
        other_values = dict()
        master_product = dict()
        signatory = docs.company_id.signatory_delivery_slip.name
        lang_code = self.env.context.get('lang') or self.env.user.lang
        lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', lang_code)])
        for doc in docs:
            sale_order = self.env['sale.order'].search([('name', '=', doc.invoice_origin)])
            current_other_values = {
                'total_amount_text': doc.currency_id.amount_to_text(doc.amount_total),
                'down_payment_amount': sale_order.down_payment_amount,
                'down_payment_amount_text': doc.currency_id.amount_to_text(sale_order.down_payment_amount),
                'remaining_amount': sale_order.remaining_amount,
                'remaining_amount_text': doc.currency_id.amount_to_text(sale_order.remaining_amount),
                'total_installment': sale_order.total_no_installment,
                'total_installment_text': num2words(sale_order.total_no_installment, lang=lang.iso_code),
                'phase1_each_installment': sale_order.phase1_each_installment,
                'phase1_each_installment_text': doc.currency_id.amount_to_text(sale_order.phase1_each_installment),
                'month_of_warranty': sale_order.month_of_warranty,
            }
            other_values[str(doc.id)] = current_other_values
            picking_no = ', '.join(sale_order.picking_ids.mapped('name'))
            picking_names[str(doc.id)] = picking_no
            shipping_address = doc.partner_id.address_get(['delivery'])['delivery']
            if shipping_address:
                shipping_address = self.env['res.partner'].browse(shipping_address)
            if not shipping_address:
                shipping_address = doc.partner_id
            shipping_addresses[str(doc.id)] = shipping_address[0]

            title_partner = doc.partner_id.child_ids.filtered(lambda child: child.title.name == 'Managing Director')
            if not title_partner:
                title_partner = doc.partner_id
            title_partners[str(doc.id)] = title_partner[0]

            payment_text = ''
            payment_text += "{}, {}, {}, {}".format(
                doc.partner_id.name, doc.partner_id.street, doc.partner_id.city, doc.partner_id.country_id.name
            )
            payment_text += ' has paid '
            # payment_text += f"{doc.currency_id.name} {current_other_values['down_payment_amount']}/= ({current_other_values['down_payment_amount_text']})"
            payment_text += "{} {}/= ({})".format(
                doc.currency_id.name, current_other_values['down_payment_amount'],
                current_other_values['down_payment_amount_text']
            )
            payment_text += " to 'MPL' as down payment and will pay rest of the amount of "
            # payment_text += f"{doc.currency_id.name} {current_other_values['remaining_amount']}/= ({current_other_values['remaining_amount_text']})"
            payment_text += "{} {}/= ({})".format(
                doc.currency_id.name, current_other_values['remaining_amount'],
                current_other_values['remaining_amount_text']
            )
            # payment_text += f" through {current_other_values['total_installment']} ({current_other_values['total_installment_text']}) installments. "
            payment_text += " through {} ({}) installments. ".format(
                current_other_values['total_installment'], current_other_values['total_installment_text']
            )
            # payment_text += ""
            if sale_order.phase1_each_installment:
                # payment_text += f"1st to {self.convert_to_ordinal(sale_order.phase1_installment_no)} installment @{doc.currency_id.name} {sale_order.phase1_each_installment}/= ({doc.currency_id.amount_to_text(sale_order.phase1_each_installment)}) per month. "
                payment_text += "1st to {} installment @{} {}/= ({}) per month. ".format(
                    self.convert_to_ordinal(sale_order.phase1_installment_no),
                    doc.currency_id.name,
                    sale_order.phase1_each_installment,
                    doc.currency_id.amount_to_text(sale_order.phase1_each_installment)
                )
            if sale_order.phase2_each_installment:
                # payment_text += f" And {self.convert_to_ordinal(sale_order.phase2_init_installment_no)} to {self.convert_to_ordinal(sale_order.phase2_installment_no)} installment @{doc.currency_id.name} {sale_order.phase2_each_installment}/= ({doc.currency_id.amount_to_text(sale_order.phase2_each_installment)}) per month."
                payment_text += " And {} to {} installment @{} {}/= ({}) per month.".format(
                    self.convert_to_ordinal(sale_order.phase2_init_installment_no),
                    self.convert_to_ordinal(sale_order.phase2_installment_no),
                    doc.currency_id.name,
                    sale_order.phase2_each_installment,
                    doc.currency_id.amount_to_text(sale_order.phase2_each_installment)
                )
            if sale_order.last_installment_amount:
                # payment_text += f" And last {self.convert_to_ordinal(sale_order.total_no_installment)} installment @{doc.currency_id.name} {sale_order.last_installment_amount}/= ({doc.currency_id.amount_to_text(sale_order.last_installment_amount)})"
                payment_text += " And last {} installment @{} {}/= ({})".format(
                    self.convert_to_ordinal(sale_order.total_no_installment),
                    doc.currency_id.name,
                    sale_order.last_installment_amount,
                    doc.currency_id.amount_to_text(sale_order.last_installment_amount)
                )
            current_other_values['payment_text'] = payment_text
            current_other_values['note'] = sale_order.note
            warranty_condition_text = []
            for template in sale_order.quotation_template_ids:
                warranty_condition_text.append(template.warranty_condition)
            current_other_values['warranty_condition'] = warranty_condition_text
            print(warranty_condition_text)

            master_product[str(doc.id)] = sale_order.order_line.filtered(lambda item: item.is_master_product).mapped('product_id').ids


        return {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'report_type': data.get('report_type') if data else '',
            'docs': docs,
            'picking_names': picking_names,
            'report_title': 'Customer Copy',
            'shipping_addresses': shipping_addresses,
            'title_partners': title_partners,
            'signatory': signatory or '',
            'show_report_title': False,
            'other_values': other_values,
            'master_product': master_product
        }
