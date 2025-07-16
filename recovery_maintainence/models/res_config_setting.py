from odoo import fields, models, api


class ResConfigMaintenance(models.TransientModel):
    _inherit = 'res.config.settings'

    service_bill_approver_1 = fields.Char(config_parameter='recovery.service_bill_approver_1')
    service_bill_approver_1_post = fields.Char(config_parameter='recovery.service_bill_approver_1_post', default='')
    service_bill_approver_1_mobile = fields.Char(config_parameter='recovery.service_bill_approver_1_mobile', default='')
    service_bill_approver_2 = fields.Char(config_parameter='recovery.service_bill_approver_2')
    service_bill_approver_2_post = fields.Char(config_parameter='recovery.service_bill_approver_2_post', default='')
    service_bill_approver_2_mobile = fields.Char(config_parameter='recovery.service_bill_approver_2_mobile', default='')
    service_bill_approver_3 = fields.Char(config_parameter='recovery.service_bill_approver_3')
    service_bill_approver_3_post = fields.Char(config_parameter='recovery.service_bill_approver_3_post', default='')
    service_bill_approver_3_mobile = fields.Char(config_parameter='recovery.service_bill_approver_3_mobile', default='')

