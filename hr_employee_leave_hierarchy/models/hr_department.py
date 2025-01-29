# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import AccessError, UserError, ValidationError
from lxml import etree
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
import pytz

class HrLeaveHierarchy(models.Model):
    _name = 'leave.hierarchy'
    _order = 'write_date desc, sequence asc'

#     @api.onchange('group_id')
#     def get_user_domain(self):
#         if self.group_id:
#             return {'domain':{'user_ids':[('id','in',self.group_id.users.ids)]}}
#         return {'domain':{'user_ids':[('in','in',[])]}}
    
    sequence = fields.Integer("Sequence")
    group_id = fields.Many2one('res.groups', string="Groups")
    user_ids = fields.Many2many('res.users')
    department_id = fields.Many2one('hr.department')

class HrEmployee(models.Model):
    _inherit = 'hr.department'

    hod_ids = fields.Many2many('res.users')
    leave_hir_ids = fields.One2many('leave.hierarchy','department_id',string="Leave Approval Hierarchy")
    
class HrLeave(models.Model):
    _inherit = 'hr.leave'

    approval_ids = fields.Many2many('res.users')
    leave_last_approver_id = fields.Many2one('res.users')
    approval_seq = fields.Integer("Approval Sequence")

    def _display_approve_button(self):
        for rec in self:
            leave_last_approver = ''
            if rec.leave_last_approver_id:
                leave_last_approver += str(rec.all_approver)
                if rec.approval_ids:
                    leave_last_approver += " <br/>Waiting approval from: "
                    for one_approval in rec.approval_ids:
                        leave_last_approver += str(one_approval.name)+", "
            rec.leave_last_approver = leave_last_approver
            rec.display_approve_button = False
            rec.display_hod_approve_button = False
            if rec.department_id and rec.state == 'confirm' and self.env.user.id in rec.sudo().approval_ids.ids:
                rec.display_approve_button = True
                last_seq = self.env['leave.hierarchy'].search([('department_id', 'in', [self.department_id.id])], limit=1, order='write_date desc, sequence desc')
                leave_hierarchy_sequence = self.department_id and self.department_id.leave_hir_ids and self.department_id.leave_hir_ids[self.approval_seq] or False

                if rec.department_id.hod_ids and self.env.user.id not in rec.department_id.hod_ids.ids and leave_hierarchy_sequence and last_seq and leave_hierarchy_sequence.id == last_seq.id:
                    rec.display_hod_approve_button = True

    display_approve_button = fields.Boolean(string='display_approve_button', compute='_display_approve_button')
    display_hod_approve_button = fields.Boolean(string='display_hod_approve_button', compute='_display_approve_button')
    leave_last_approver = fields.Html(string='Last Approval String', compute='_display_approve_button')
    all_approver = fields.Html(string='Approval String')

    def action_send_to_hod(self):
        if self.department_id:
            self.approval_ids = [(6, 0, self.department_id.hod_ids.ids)]
            self.message_post(body=_("<p><strong><span class='fa fa-sun-o'></span></strong> <span>Leaves Send to HOD.</span></p>"))
            if self.approval_ids:
                self.env.ref('hr_employee_leave_hierarchy.leave_request_mail').send_mail(self.id, force_send=True)

    def action_approve(self):
        self.ensure_one()
        # self._check_security_action_approve()
        if self.department_id:
            leave_hierarchy_sequences = self.department_id and self.department_id.leave_hir_ids and self.department_id.leave_hir_ids[self.approval_seq+1] if self.approval_seq+1 < len(self.department_id.leave_hir_ids) else False
            if leave_hierarchy_sequences and leave_hierarchy_sequences.user_ids:
                self.leave_last_approver_id = self.env.user.id
                now_timezone1 = pytz.UTC.localize(datetime.now()).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
                start_date = datetime.strptime(fields.Datetime.to_string(now_timezone1), "%Y-%m-%d %H:%M:%S")
                if self.all_approver:
                    self.all_approver += " <br/>Approved by : " + str(self.env.user.name) + " At " + str(start_date)
                if not self.all_approver:
                    self.all_approver = " <br/>Approved by : " + str(self.env.user.name) + " At " + str(start_date)
                self.approval_ids = [(6, 0, leave_hierarchy_sequences.user_ids.ids)]
                self.approval_seq = self.approval_seq+1
                self.message_post(body=_("<p><strong><span class='fa fa-sun-o'></span></strong> <span>Leaves Approval</span> done by <span> " + str(self.env.user.name) + "</span></p>"))
                if self.approval_ids:
                    self.env.ref('hr_employee_leave_hierarchy.leave_request_mail').send_mail(self.id, force_send=True)
                return True
            else:
                now_timezone1 = pytz.UTC.localize(datetime.now()).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
                start_date = datetime.strptime(fields.Datetime.to_string(now_timezone1), "%Y-%m-%d %H:%M:%S")
                if self.all_approver:
                    self.all_approver += " <br/>Approved by : " + str(self.env.user.name) + " At " + str(start_date)
                if not self.all_approver:
                    self.all_approver = " <br/>Approved by : " + str(self.env.user.name) + " At " + str(start_date)

        self.leave_last_approver_id = self.env.user.id
        self.approval_ids = False

        return super(HrLeave, self).action_approve()

    @api.model
    def create(self, values):
        res = super(HrLeave, self).create(values)
        if not res.department_id:
            raise ValidationError(_('Please add department for %s Employee.' %(res.employee_id.name)))
        leave_hierarchy_sequences = res.department_id and res.department_id.leave_hir_ids and res.department_id.leave_hir_ids[0] if res.approval_seq+1 <= len(res.department_id.leave_hir_ids) else False
        if leave_hierarchy_sequences and leave_hierarchy_sequences.user_ids:
            res.approval_ids = [(6,0,leave_hierarchy_sequences.user_ids.ids)]
            res.approval_seq = 0
            if res.approval_ids:
                self.env.ref('hr_employee_leave_hierarchy.leave_request_mail').send_mail(res.id, force_send=True)
        if not leave_hierarchy_sequences.user_ids:
            raise ValidationError(_('Please ensure the employee \'s department and leave type \
                  have been specified in the leave approval configuration'))
        return res
