from odoo import fields, models, api


class SaleOrderBillReport(models.AbstractModel):
    _name = 'report.film_sale_order.report_sales_order_bill'
    _description = 'Sale Order Bill Report'

    @api.model
    def _get_report_values(self, docids, data=None):

        model = self.env['sale.order']
        ids = self.env.context.get('active_ids') or False
        docs = model.browse(docids)
        amount_str_dict = {}
        return {
            'docs': docs,
            'doc_ids': docids,
        }
