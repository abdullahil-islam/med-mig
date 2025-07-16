from odoo import fields, models, api


class ServiceBillReport(models.AbstractModel):
    _name = 'report.recovery_maintainence.report_medionics_service_bill'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)
        service_bill_approver_1 = self.env['ir.config_parameter'].sudo().get_param("recovery.service_bill_approver_1")
        service_bill_approver_1_post = self.env['ir.config_parameter'].sudo().get_param("recovery.service_bill_approver_1_post")
        service_bill_approver_1_mobile = self.env['ir.config_parameter'].sudo().get_param("recovery.service_bill_approver_1_mobile")
        service_bill_approver_2 = self.env['ir.config_parameter'].sudo().get_param("recovery.service_bill_approver_2")
        service_bill_approver_2_post = self.env['ir.config_parameter'].sudo().get_param("recovery.service_bill_approver_2_post")
        service_bill_approver_2_mobile = self.env['ir.config_parameter'].sudo().get_param("recovery.service_bill_approver_2_mobile")
        service_bill_approver_3 = self.env['ir.config_parameter'].sudo().get_param("recovery.service_bill_approver_3")
        service_bill_approver_3_post = self.env['ir.config_parameter'].sudo().get_param("recovery.service_bill_approver_3_post")
        service_bill_approver_3_mobile = self.env['ir.config_parameter'].sudo().get_param("recovery.service_bill_approver_3_mobile")

        return {
            'docs': docs,
            'service_bill_approver_1': service_bill_approver_1 or '',
            'service_bill_approver_1_post': service_bill_approver_1_post or '',
            'service_bill_approver_1_mobile': service_bill_approver_1_mobile or '',
            'service_bill_approver_2': service_bill_approver_2 or '',
            'service_bill_approver_2_post': service_bill_approver_2_post or '',
            'service_bill_approver_2_mobile': service_bill_approver_2_mobile or '',
            'service_bill_approver_3': service_bill_approver_3 or '',
            'service_bill_approver_3_post': service_bill_approver_3_post or '',
            'service_bill_approver_3_mobile': service_bill_approver_3_mobile or '',
        }
