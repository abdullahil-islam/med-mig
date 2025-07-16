# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, models, modules, _
import pytz


# class MaintenanceRequest(models.Model):
#     _name = 'maintenance.request'
#     _inherit = ['maintenance.request', 'mail.thread', 'mail.activity.mixin']
#
#
# class Repair(models.Model):
#     _name = 'repair.order'
#     _inherit = ['repair.order', 'mail.thread', 'mail.activity.mixin']


class Users(models.Model):
    _inherit = 'res.users'

    @api.model
    def systray_get_activities(self):
        res = super(Users, self).systray_get_activities()
        # For Maintenance Request.
        today_date = datetime.now().astimezone(pytz.timezone(self.env.context.get('tz'))).date()
        maintenance_count = self.env['maintenance.request'].search_count(
            [['reminder_time', '!=', False],
             ['reminder_time', '=', today_date]])
        model = self.env['ir.model'].search([('model', '=', 'maintenance.request')])
        maintenance_systray = {
            'id': model.id,
            'type': 'document_expiry',
            'name': _("Maintenance Request"),
            'model': 'maintenance.request',
            'icon': modules.module.get_module_icon(
                'transport_document_notification'),
            'total_count': maintenance_count,
            'date_deadline': today_date,
        }
        res.insert(0, maintenance_systray)
        # For New Repair Order Request.
        repair_count = self.env['repair.order'].search_count(
            [['is_new_request', '=', True],
             ['type', '=', False]])
        model = self.env['ir.model'].search([('model', '=', 'repair.order')])
        repair_systray = {
            'id': model.id,
            'type': 'new_repaird_order',
            'name': _("New Repair Order"),
            'model': 'repair.order',
            'icon': modules.module.get_module_icon(
                'transport_document_notification'),
            'total_count': repair_count,
            'date_deadline': today_date,
        }
        res.insert(0, repair_systray)
        return res
