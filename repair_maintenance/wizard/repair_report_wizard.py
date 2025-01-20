from odoo import api, fields, models, _


class RepairOrderReport(models.AbstractModel):
    _name = 'report.repair_maintenance.report_repair_order'
    _description = "Repair Order Report"

    def _get_customer_datas(self, data):
        machine_datas = []
        all_user = []
        if data['form']['all_partner'] == True:
            all_user = self.env['res.partner'].search([])
        if data['form']['partner_id'] and data['form']['all_partner'] == False:
            all_user = self.env['res.partner'].search([('id','=',data['form']['partner_id'][0])]) 
        for user in all_user:
            repair_orders = self.env['repair.order'].sudo().search([('scheduled_date', '>=', data['form']['from_date']),
            ('scheduled_date', '<=', data['form']['to_date']), ('partner_id', '=', user.id)])
            if repair_orders:
                final_data = [{'from_date':data['form']['from_date'],'to_date':data['form']['to_date'],'partner_id':user.name,'count':len(repair_orders.ids)}]
                row_data = []
                for order in repair_orders:
                    technician = ''
                    for onetec in order.technician_id:
                        technician += onetec.name + ', '
                    row_data.append({'serial_number': order.name,
                                           'product': order.product_id and order.product_id.name or '',
                                           'type': order.type,
                                           'valid_from': order.from_date and order.from_date.strftime('%d.%m.%Y') or '',
                                           'valid_to': order.to_date and order.to_date.strftime('%d.%m.%Y') or '',
                                           'technician': technician,})
                final_data[0]['machine_datas'] = row_data
                machine_datas.append(final_data)
        return machine_datas

    def _get_machine_datas(self, data):
        machine_datas = []
        all_user = []
        if data['form']['all_product'] == True:
            all_user = self.env['product.product'].search([])
        if data['form']['product_id'] and data['form']['all_product'] == False:
            all_user = self.env['product.product'].search([('id','=',data['form']['product_id'][0])]) 
        for user in all_user:
            repair_orders = self.env['repair.order'].sudo().search([('scheduled_date', '>=', data['form']['from_date']),
            ('scheduled_date', '<=', data['form']['to_date']), ('product_id', '=', user.id)])
            if repair_orders:
                final_data = [{'from_date':data['form']['from_date'],'to_date':data['form']['to_date'],'product_id':user.name,'count':len(repair_orders.ids)}]
                row_data = []
                for order in repair_orders:
                    technician = ''
                    for onetec in order.technician_id:
                        technician += onetec.name + ', '
                    row_data.append({'serial_number': order.name,
                                           'partner': order.partner_id and order.partner_id.name or '',
                                           'type': order.type,
                                           'valid_from': order.from_date and order.from_date.strftime('%d.%m.%Y') or '',
                                           'valid_to': order.to_date and order.to_date.strftime('%d.%m.%Y') or '',
                                           'technician': technician,
                                          })
                final_data[0]['machine_datas'] = row_data
                machine_datas.append(final_data)
        return machine_datas

    def _get_engineer_datas(self, data):
        machine_datas = []
        all_user = []
        if data['form']['all_technician'] == True:
            all_user = self.env['res.users'].search([])
        if data['form']['technician_id'] and data['form']['all_technician'] == False:
            all_user = self.env['res.users'].search([('id','=',data['form']['technician_id'][0])]) 
        for user in all_user:
            repair_orders = self.env['repair.order'].sudo().search([('scheduled_date', '>=', data['form']['from_date']),
            ('scheduled_date', '<=', data['form']['to_date']), ('technician_id', '=', user.id)])
            if repair_orders:
                final_data = [{'from_date':data['form']['from_date'],'to_date':data['form']['to_date'],'technician_id':user.name,'count':len(repair_orders.ids)}]
                row_data = []
                for order in repair_orders:
                    row_data.append({'serial_number': order.name,
                                          'product': order.product_id and order.product_id.name or '',
                                          'partner': order.partner_id and order.partner_id.name or '',
                                          'type': order.type,
                                          'visit_date': order.scheduled_date and order.scheduled_date.strftime('%d.%m.%Y') or ''})
                final_data[0]['machine_datas'] = row_data
                machine_datas.append(final_data)
        return machine_datas

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        all_dict_val = []
        if data['form']['based_on'] == 'customer':
            all_dict_val = self._get_customer_datas
        if data['form']['based_on'] == 'machine':
            all_dict_val = self._get_machine_datas
        if data['form']['based_on'] == 'engineer':
            all_dict_val = self._get_engineer_datas
        return {
            'doc_ids': docids,
            'doc_model': model,
            'data': data,
            'docs': docs,
            'all_dict_val': all_dict_val,
        }


class RepairReportWizard(models.TransientModel):
    _name = 'repair.report.wizard'
    _description = "Repair Report Wizard"

    based_on = fields.Selection([
    ('customer', 'Customer Wise'),
    ('machine', 'Machine Wise'),
    ('engineer', 'Engineer Wise')], string="Printing Based On", default="customer")
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    partner_id = fields.Many2one('res.partner', 'Customer')
    product_id = fields.Many2one('product.product', string='Machine')
    technician_id = fields.Many2one('res.users', string='Engineer')
    all_partner = fields.Boolean("All Customer")
    all_product = fields.Boolean("All Machine")
    all_technician = fields.Boolean("All Engineer")

    def print_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.ids
        data['model'] = 'repair.report.wizard'
        data['form'] = self.read([
        'based_on', 'partner_id', 'product_id', 'technician_id',
        'from_date', 'to_date','all_partner','all_product','all_technician'])[0]
        return self.env.ref('repair_maintenance.action_report_repair_order')\
            .with_context(landscape=True).report_action(self, data=data)

