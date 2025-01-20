# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import AccessError, UserError, ValidationError
from dateutil.relativedelta import relativedelta
from lxml import etree

class EmpFree(models.Model):
    
    _name = 'free.employee'
    _description = 'Free Employee'
    
    name = fields.Char("Name")
    
    
    def get_free_emp_eng(self, assigned_eng):
        for rec in self:
            all_emp = self.env['hr.employee'].search([('user_id','!=', False)])
            emp_list = []
            for emp in all_emp:
                if emp.user_id.has_group('repair_maintenance.group_maintenance_technician') and emp.user_id.id not in assigned_eng:
                    emp_list.append(emp.id)
            return emp_list
    
    
    def get_notfree_emp_eng(self, assigned_eng):
        for rec in self:
            all_emp = self.env['hr.employee'].search([('user_id','!=', False)])
            emp_list = []
            for emp in all_emp:
                if emp.user_id.has_group('repair_maintenance.group_maintenance_technician') and emp.user_id.id in assigned_eng:
                    emp_list.append(emp.id)
            return emp_list
        
    
    def get_startedwork_emp_eng(self, apps):
        for rec in self:
            project = self.env['project.task'].search([('x_project_task_start_date','!=', False),('x_project_task_end_date','=', False)])
            maintanance = self.env['maintenance.request'].search([('x_maintenance_start_date','!=', False),('x_maintenance_end_date','=', False)])
            repair = self.env['repair.order'].search([('start_repair_date','!=', False),('end_repair_date','=', False)])
            assigned_eng = []
            if apps == 'all':
                for pr in project:
                    assigned_eng.extend(pr.user_ids.ids)
                for mt in maintanance:
                    assigned_eng.extend(mt.user_ids.ids)
                for re in repair:
                    assigned_eng.extend(re.technician_id.ids)
                    assigned_eng.extend(re.inloop_ids.ids)
            if apps == 'project':
                for pr in project:
                    assigned_eng.extend(pr.user_ids.ids)
            if apps == 'maintenance':
                for mt in maintanance:
                    assigned_eng.extend(mt.user_ids.ids)
            if apps == 'repair':
                for re in repair:
                    assigned_eng.extend(re.technician_id.ids)
                    assigned_eng.extend(re.inloop_ids.ids)
            return list(set(assigned_eng))
        
    
    def get_only_assigned_emp_eng(self, apps):
        for rec in self:
            project = self.env['project.task'].search([('x_project_task_start_date','=', False),('x_project_task_end_date','=', False)])
            maintanance = self.env['maintenance.request'].search([('x_maintenance_start_date','=', False),('x_maintenance_end_date','=', False)])
            repair = self.env['repair.order'].search([('start_repair_date','=', False),('end_repair_date','=', False)])
            assigned_eng = []
            if apps == 'all':
                for pr in project:
                    assigned_eng.extend(pr.user_ids.ids)
                for mt in maintanance:
                    assigned_eng.extend(mt.user_ids.ids)
                for re in repair:
                    assigned_eng.extend(re.technician_id.ids)
                    assigned_eng.extend(re.inloop_ids.ids)
            if apps == 'project':
                for pr in project:
                    assigned_eng.extend(pr.user_ids.ids)
            if apps == 'maintenance':
                for mt in maintanance:
                    assigned_eng.extend(mt.user_ids.ids)
            if apps == 'repair':
                for re in repair:
                    assigned_eng.extend(re.technician_id.ids)
                    assigned_eng.extend(re.inloop_ids.ids)
            return list(set(assigned_eng))
        
    
    def open_action_call(self, employee):
        for rec in self:
            action = self.env.ref('hr.open_view_employee_list_my').read()[0]
            action['domain'] = [('id','in',employee)]
            action['context'] = {'group_by':'department_id'}
            return action
        
    
    def get_free_eng(self):
        for rec in self:
            assigned_eng = rec.get_startedwork_emp_eng('all')
            free_emp = rec.get_free_emp_eng(assigned_eng)
            return rec.open_action_call(free_emp)
            
    
    def get_started_work_eng(self):
        for rec in self:
            assigned_eng = rec.get_startedwork_emp_eng('all')
            return rec.open_action_call(rec.get_notfree_emp_eng(assigned_eng))
            
    
    def get_assigned_eng(self):
        for rec in self:
            assigned_eng = rec.get_only_assigned_emp_eng('all')
            return rec.open_action_call(rec.get_notfree_emp_eng(assigned_eng))
            
    
    def only_assign_eng_repair(self):
        for rec in self:
            assigned_eng = rec.get_only_assigned_emp_eng('repair')
            return rec.open_action_call(rec.get_notfree_emp_eng(assigned_eng))
            
    
    def started_work_repair(self):
        for rec in self:
            assigned_eng = rec.get_startedwork_emp_eng('repair')
            return rec.open_action_call(rec.get_notfree_emp_eng(assigned_eng))
            
    
    def only_assign_eng_maintenenance(self):
        for rec in self:
            assigned_eng = rec.get_only_assigned_emp_eng('maintenance')
            return rec.open_action_call(rec.get_notfree_emp_eng(assigned_eng))
            
    
    def started_work_maintenance(self):
        for rec in self:
            assigned_eng = rec.get_startedwork_emp_eng('maintenance')
            return rec.open_action_call(rec.get_notfree_emp_eng(assigned_eng))
            
    
    def only_assign_eng_task(self):
        for rec in self:
            assigned_eng = rec.get_only_assigned_emp_eng('project')
            return rec.open_action_call(rec.get_notfree_emp_eng(assigned_eng))
            
    
    def started_work_task(self):
        for rec in self:
            assigned_eng = rec.get_startedwork_emp_eng('project')
            return rec.open_action_call(rec.get_notfree_emp_eng(assigned_eng))

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    pass_exp_date = fields.Date(string="Passport Expiry Date")
    certificate = fields.Selection([
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('mba', 'MBA'),
        ('diploma', 'Diploma'),
    ], 'Certificate Level', default='master', groups="hr.group_hr_user")
    
    @api.model
    def _cron_passport_expiry_date(self):
        pass_exp = self.search([('passport_id', '!=', False), ('pass_exp_date', '=', fields.Date.to_string(fields.Datetime.today().date() + relativedelta(months=1)))])
        for one_emp in pass_exp:
            self.env.ref('repair_maintenance.new_passport_expiry_date_email_template').send_mail(one_emp.id, force_send=True)

