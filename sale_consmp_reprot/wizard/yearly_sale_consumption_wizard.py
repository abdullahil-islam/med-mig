from odoo import models, fields, api
from datetime import datetime
import io
import base64
import xlsxwriter

class SaleYearlyReportWizard(models.TransientModel):
    _name = 'sale.yearly.report.wizard'
    _description = 'Wizard to Generate Sale Order Excel Report'

    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    file_data = fields.Binary('Excel File')
    file_name = fields.Char('File Name')

    def action_generate_report(self):
        domain = [
            ('date_order', '>=', self.start_date),
            ('date_order', '<=', self.end_date),
            ('state', 'in', ['sale', 'done']),
        ]
        orders = self.env['sale.order'].search(domain)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Sale Orders')

        # Report Header
        header_format = workbook.add_format({'bold': True, 'font_size': 25, 'align': 'center'})
        sheet.merge_range("A2:K3", "Yearly Sale Consumption Report", header_format)

        bold = workbook.add_format({'bold': True})
        headers = ['Date', 'Customer Name', 'Thana/Area', 'District', 'Division']
        headers += orders.order_line.mapped('product_id').mapped('name')
        headers.append('Total')

        row = 5
        for col, header in enumerate(headers):
            sheet.write(row, col, header, bold)
        row += 1
        col = 0
        for order in orders:
            sheet.write(row, col, order.date_order.strftime('%Y-%m-%d'))
            col += 1
            sheet.write(row, col, order.partner_id.name)
            col += 1
            sheet.write(row, col, order.partner_id.sub_city_id.name or '')
            col += 1
            sheet.write(row, col, order.partner_id.city_id.name or '')
            col += 1
            sheet.write(row, col, order.partner_id.state_id.name or '')
            # col += 1
            # sheet.write(row, col, order.name)
            # col += 1
            # sheet.write(row, col, order.amount_total)
            total = 0
            for line in order.order_line:
                if line.product_id.name in headers:
                    col = headers.index(line.product_id.name)
                    sheet.write(row, col, line.product_uom_qty)
                    total += line.product_uom_qty
            sheet.write(row, len(headers)-1, total)
            col = 0
            row += 1

        workbook.close()
        output.seek(0)
        file_content = output.read()
        output.close()

        self.file_data = base64.b64encode(file_content)
        self.file_name = f'SaleOrders_{self.start_date}_{self.end_date}.xlsx'

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.yearly.report.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
