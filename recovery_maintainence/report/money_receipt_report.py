from odoo import fields, models, api
import textwrap


class MoneyReceiptReport(models.AbstractModel):
    _name = 'report.recovery_maintainence.report_money_receipt_view'
    _description = 'Money Receipt Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env['account.payment']
        ids = self.env.context.get('active_ids') or False
        docs = model.browse(docids)
        amount_str_dict = {}
        for doc in docs:
            amount_in_words = doc.currency_id.amount_to_text(doc.amount)
            wrapped_text = textwrap.fill(amount_in_words, width=75).split('\n')
            print(wrapped_text)
            amount_str_dict[str(doc.id)] = wrapped_text
        return {
            'docs': docs,
            'doc_ids': docids,
            'data': {'report_name': 'ALamin Islam'},
            'amount_str_dict': amount_str_dict,
        }
