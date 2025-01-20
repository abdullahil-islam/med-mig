from odoo import api, fields, models, _


class MaintenanceRequestReport(models.AbstractModel):
    _name = 'report.repair_maintenance.report_maintenance_request'
    _description = "Maintenance Request Report"

    def _get_customer_datas(self, data):
        customer_datas = []
        if data['form']['partner_id']:
            maintenance_record = self.env['maintenance.request'].sudo().search([('schedule_date', '>=', data['form']['from_date']),
            ('schedule_date', '<=', data['form']['to_date']), ('partner_id', '=', data['form']['partner_id'][0])])
            for order in maintenance_record:
                customer_datas.append({'serial_number': order.name,
                                       'product': order.equipment_id and order.equipment_id.name or '',
                                       'type': order.type,
                                       'valid_from': order.from_date and order.from_date.strftime('%d.%m.%Y') or '',
                                       'valid_to': order.to_date and order.to_date.strftime('%d.%m.%Y') or ''})
        return customer_datas

    def _get_machine_datas(self, data):
        machine_datas = []
        if data['form']['product_id']:
            maintenance_record = self.env['maintenance.request'].sudo().search([('schedule_date', '>=', data['form']['from_date']),
            ('schedule_date', '<=', data['form']['to_date']), ('equipment_id', '=', data['form']['product_id'][0])])
            for order in maintenance_record:
                machine_datas.append({'serial_number': order.name,
                                       'partner': order.partner_id and order.partner_id.name or '',
                                       'type': order.type,
                                       'valid_from': order.from_date and order.from_date.strftime('%d.%m.%Y') or '',
                                       'valid_to': order.to_date and order.to_date.strftime('%d.%m.%Y') or ''})
        return machine_datas

    def _get_engineer_datas(self, data):
        machine_datas = []
        if data['form']['technician_id']:
            maintenance_record = self.env['maintenance.request'].sudo().search([('schedule_date', '>=', data['form']['from_date']),
            ('schedule_date', '<=', data['form']['to_date']), ('user_id', '=', data['form']['technician_id'][0])])
            for order in maintenance_record:
                machine_datas.append({'serial_number': order.name,
                                      'product': order.equipment_id and order.equipment_id.name or '',
                                      'partner': order.partner_id and order.partner_id.name or '',
                                      'type': order.type,
                                      'visit_date': order.schedule_date and order.schedule_date.strftime('%d.%m.%Y') or ''})
        return machine_datas
    
    def _get_customer_count(self, data):
        customer_datas = []
        if data['form']['partner_id']:
            maintenance_record = self.env['maintenance.request'].sudo().search([('schedule_date', '>=', data['form']['from_date']),
            ('schedule_date', '<=', data['form']['to_date']), ('partner_id', '=', data['form']['partner_id'][0])])
        return len(maintenance_record)

    def _get_machine_count(self, data):
        machine_datas = []
        if data['form']['product_id']:
            maintenance_record = self.env['maintenance.request'].sudo().search([('schedule_date', '>=', data['form']['from_date']),
            ('schedule_date', '<=', data['form']['to_date']), ('equipment_id', '=', data['form']['product_id'][0])])
        return len(maintenance_record)

    def _get_engineer_count(self, data):
        machine_datas = []
        if data['form']['technician_id']:
            maintenance_record = self.env['maintenance.request'].sudo().search([('schedule_date', '>=', data['form']['from_date']),
            ('schedule_date', '<=', data['form']['to_date']), ('user_id', '=', data['form']['technician_id'][0])])
        return len(maintenance_record)

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        return {
            'doc_ids': docids,
            'doc_model': model,
            'data': data,
            'docs': docs,
            'get_customer_count': self._get_customer_count,
            'get_machine_count': self._get_machine_count,
            'get_engineer_count': self._get_engineer_count,
            'get_customer_datas': self._get_customer_datas,
            'get_machine_datas': self._get_machine_datas,
            'get_engineer_datas': self._get_engineer_datas,
        }


class MaintenanceReportWizard(models.TransientModel):
    _name = 'maintenance.report.wizard'
    _description = "Maintenance Report Wizard"

    based_on = fields.Selection([
    ('customer', 'Customer Wise'),
    ('machine', 'Machine Wise'),
    ('engineer', 'Engineer Wise')], string="Printing Based On", default="customer")
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    partner_id = fields.Many2one('res.partner', 'Customer')
    product_id = fields.Many2one('product.product', string='Machine')
    technician_id = fields.Many2one('res.users', string='Engineer')

    def print_reportx(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.ids
        data['model'] = 'maintenance.report.wizard'
        data['form'] = self.read([
        'based_on', 'partner_id', 'product_id', 'technician_id',
        'from_date', 'to_date'])[0]
        return self.env.ref('repair_maintenance.action_maintenance_request')\
            .with_context(landscape=True).report_action(self, data=data)

