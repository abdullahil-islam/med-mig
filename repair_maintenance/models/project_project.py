# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_TIME_FORMAT


class ProjectProject(models.Model):
    _inherit = "project.project"
    
    
    def calculate_duration_of_project(self):
        for rec in self:
            all_task = self.env['project.task'].search([('project_id','=', rec.id)])
            diff_dates = False
            diff_str = ''
            for task in all_task:
                end_date = False
                if not task.x_project_task_end_date:
                    end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                else:
                    end_date = task.x_project_task_end_date
                if task.x_project_task_start_date and end_date:
                    from_date = datetime.strptime(str(task.x_project_task_start_date), '%Y-%m-%d %H:%M:%S')
                    to_date = datetime.strptime(str(end_date), '%Y-%m-%d %H:%M:%S')
                    data = relativedelta(to_date, from_date)
                    if diff_dates:
                        diff_dates = diff_dates + data
                    else:
                        diff_dates = data
            if diff_dates:
                if diff_dates.years:
                    diff_str += str(diff_dates.years) + ' Years '
                if diff_dates.months:
                    diff_str += str(diff_dates.months) + ' Months '
                if diff_dates.days:
                    diff_str += str(diff_dates.days) + ' Days '
                if diff_dates.hours:
                    diff_str += str(diff_dates.hours) + ' Hours '
                if diff_dates.minutes:
                    diff_str += str(diff_dates.minutes) + ' Minutes '
                if diff_dates.seconds:
                    diff_str += str(diff_dates.seconds) + ' Seconds '
            rec.duration_of_project = diff_str
            
    
    def action_assign_to_done(self):
        for rec in self:
            rec.complete_project = True

    
    def _get_running_status(self):
        for rec in self:
            running_task = self.env['project.task'].search(
                [('project_id', '=', rec.id), ('x_project_task_start_date', '!=', False),
                 ('x_project_task_end_date', '=', False)])
            if running_task:
                rec.is_running_project = True
            else:
                rec.is_running_project = False

    def _get_running_domain(self, operator, value):
        running_task = self.env['project.task'].search(
            [('x_project_task_start_date', '!=', False), ('x_project_task_end_date', '=', False)])
        project_ids = [rec.project_id.id for rec in running_task if rec.project_id]
        return [('id', 'in', project_ids)]

    def _get_default_team_id(self):
        MT = self.env['maintenance.team']
        team = MT.search([('company_id', '=', self.env.user.company_id.id)], limit=1)
        if not team:
            team = MT.search([], limit=1)
        return team.id
    
    project = fields.Char(string="Project ID")
    project_name = fields.Char("Project Name")
    complete_project = fields.Boolean("Done Projects", default=False)
    is_running_project = fields.Boolean(string="Is Running Project", compute='_get_running_status',search='_get_running_domain', default=False)

    name_of_equipment = fields.Selection(
        [('mri', 'MRI-'), ('ct', 'CT-'), ('xr', 'XR-'), ('usg', 'USG-'), ('cr', 'CR-'), ('fpd', 'FPD-'), ('mam', 'MAM-'),
         ('bmd', 'BMD-'), ('opg', 'OPG-'), ('crm', 'CRM-'), ('prt', 'PRT-'), ('omprt', 'PRTOM-')],
        string="Name Of Equipment", required=True)
    duration_of_project = fields.Char(string="Duration of Project", compute=calculate_duration_of_project)
    maintenance_team_id = fields.Many2one('maintenance.team', string='Team')
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    tag_id = fields.Many2many('res.partner.category',related="partner_id.category_id", string="Tags")
    categoty_eq_id = fields.Many2one('maintenance.equipment.category', string="Category Of Equipment")
    eq_serial_number = fields.Char(string="Equipment Serial No.")
    project_type = fields.Selection([('govt', 'Govt.'),('private', 'Private'),('3party', '3rd Party')], string="Project Type/Tag", required=True, default='govt')
    tender_no = fields.Char('Tender Number')
    warranty = fields.Selection(
[("1y","1Y"),("2y","2Y"),("3y","3Y"),("4y","4Y"),("5y","5Y"),("6y","6Y"),("7y","7Y"),("8y","8Y"),("9y","9Y"),("nowarranty","No Warranty"),("lifetime","Life Time (Free Service)")], string="Warranty",)
    
    @api.onchange('partner_id')
    def onchange_partner(self):
        # related = 'product_id.categ_id',
        if self.partner_id:
            self.street = self.partner_id.street
            self.street2 = self.partner_id.street2
            self.zip = self.partner_id.zip
            self.city = self.partner_id.city
            self.state_id = self.partner_id.state_id and self.partner_id.state_id.id or ''
            self.country_id = self.partner_id.country_id and self.partner_id.country_id.id or ''
         
    
    def attachment_tree_view(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['domain'] = str([
            '|',
            '&',
            ('res_model', '=', 'project.project'),
            ('res_id', 'in', self.ids),
            '&',
            ('res_model', '=', 'project.task'),
            ('res_id', 'in', self.task_ids.ids)
        ])
        action['context'] = "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        return action
            
    @api.model
    def create(self, vals):
        vals['project_name'] = vals['name']
        if vals.get('name_of_equipment') == 'mri':
            vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.mri') + ',' + vals['name']
        if vals.get('name_of_equipment') == 'ct':
            vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.ct') + ',' + vals['name']
        if vals.get('name_of_equipment') == 'xr':
            vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.xr') + ',' + vals['name']
        if vals.get('name_of_equipment') == 'usg':
            vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.usg') + ',' + vals['name']
        if vals.get('name_of_equipment') == 'cr':
            vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.cr') + ',' + vals['name']
        if vals.get('name_of_equipment') == 'fpd':
            vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.fpd') + ',' + vals['name']
        if vals.get('name_of_equipment') == 'mam':
            vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.mam') + ',' + vals['name']
        if vals.get('name_of_equipment') == 'bmd':
            vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.bmd') + ',' + vals['name']
        if vals.get('name_of_equipment') == 'opg':
            vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.opg') + ',' + vals['name']
        if vals.get('name_of_equipment') == 'crm':
            vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.crm') + ',' + vals['name']
        if vals.get('name_of_equipment') == 'prt':
            vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.prt') + ',' + vals['name']
        if vals.get('name_of_equipment') == 'omprt':
            vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.omprt') + ',' + vals['name']
        # if values.get('name_of_equipment') and values.get('sequence'):
        #     values['name'] = values.get('sequence')+ '/' + values['name']
        #     values['name'] = dict(self.fields_get(allfields=['name_of_equipment'])['name_of_equipment']['selection'])[values.get('name_of_equipment')]+ '/' + values['name']
        res = super(ProjectProject, self).create(vals)
        if res.maintenance_team_id and res.maintenance_team_id.member_ids:
            for line in res.maintenance_team_id.member_ids:
                exist = self.env['mail.followers'].sudo().search([('res_id','=', res.id),('partner_id','=', line.partner_id.id)])
                if not exist:
                    self.env['mail.followers'].sudo().create({
                    'res_id': res.id,
                    'res_model': 'project.project',
                    'partner_id': line.partner_id.id,
                    })
            
        return res
    
    
    def write(self, vals):
        res = super(ProjectProject, self).write(vals)
        return res


#
class ProjectTask(models.Model):
    _inherit = "project.task"

    
    def action_star_task(self):
        for rec in self:
            self.write({'x_project_task_start_date': fields.Datetime.now()})
            now_timezone = pytz.UTC.localize(rec.x_project_task_start_date).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
            aa = datetime.strptime(fields.Datetime.to_string(now_timezone), "%Y-%m-%d %H:%M:%S")
            if rec.name == 'Commissioning & Demonstration':
                self.env.ref('repair_maintenance.new_equipment_email_template').with_context(start_time=aa,end_time='').send_mail(rec.id, force_send=True)

    
    def action_end_task(self):
        for rec in self:
            self.write({'x_project_task_end_date': fields.Datetime.now()})
            now_timezone1 = pytz.UTC.localize(rec.x_project_task_start_date).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
            aa1 = datetime.strptime(fields.Datetime.to_string(now_timezone1), "%Y-%m-%d %H:%M:%S")
            now_timezone = pytz.UTC.localize(rec.x_project_task_end_date).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
            aa = datetime.strptime(fields.Datetime.to_string(now_timezone), "%Y-%m-%d %H:%M:%S")
            if rec.name == 'Commissioning & Demonstration':
                self.env.ref('repair_maintenance.new_equipment_email_template').with_context(end_time=aa, start_time=aa1).send_mail(rec.id, force_send=True)


    
    def calculate_duration_of_task(self):
        for rec in self:
            end_date = False
            if not rec.x_project_task_end_date:
                end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:
                end_date = rec.x_project_task_end_date
            diff_str = ''
            if rec.x_project_task_start_date and end_date:
                from_date = datetime.strptime(str(rec.x_project_task_start_date), '%Y-%m-%d %H:%M:%S')
                to_date = datetime.strptime(str(end_date), '%Y-%m-%d %H:%M:%S')
                diff_dates = relativedelta(to_date, from_date)
                if diff_dates.years:
                    diff_str += str(diff_dates.years) + ' Years '
                if diff_dates.months:
                    diff_str += str(diff_dates.months) + ' Months '
                if diff_dates.days:
                    diff_str += str(diff_dates.days) + ' Days '
                if diff_dates.hours:
                    diff_str += str(diff_dates.hours) + ' Hours '
                if diff_dates.minutes:
                    diff_str += str(diff_dates.minutes) + ' Minutes '
                if diff_dates.seconds:
                    diff_str += str(diff_dates.seconds) + ' Seconds '
            rec.duration_of_task = diff_str

    x_project_task_start_date = fields.Datetime(string="Start Date")
    x_project_task_end_date = fields.Datetime(string="End Date")
    duration_of_task = fields.Char(string="Duration of Task", compute=calculate_duration_of_task)
    user_ids = fields.Many2many('res.users', string="Assigned to")

    
    def action_send_mail(self):
        # self.env.ref('repair_maintenance.project_task_assigned_email_template').send_mail(self.id, force_send=True)
        template_engineer = self.env.ref('repair_maintenance.project_task_assigned_email_template', False)
        if self.user_ids:
            start_date = ''
            end_date = ''
            if self.x_project_task_start_date:
                now_timezone1 = pytz.UTC.localize(self.x_project_task_start_date).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
                start_date = datetime.strptime(fields.Datetime.to_string(now_timezone1), "%Y-%m-%d %H:%M:%S")
            if self.x_project_task_end_date:
                now_timezone = pytz.UTC.localize(self.x_project_task_end_date).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
                end_date = datetime.strptime(fields.Datetime.to_string(now_timezone), "%Y-%m-%d %H:%M:%S")
            template_engineer.with_context(end_time=end_date, start_time=start_date).send_mail(self.id, force_send=True,
                                        email_values={'email_to': ','.join(self.user_ids.mapped('email'))})

        return True
    
    
    def write(self, vals):
        result = super(ProjectTask, self).write(vals)
        if self.x_project_task_end_date and self.kanban_state != 'done':
            self.kanban_state = 'done'
        return result

            # user_id = fields.Many2many('res.users',
        #     string='Assigned to',
        #     default=lambda self: self.env.uid,
        #     index=True, track_visibility='always')  #
#     
#     def equipment_create(self, vals):
#         maintenance = self.env['maintenance.equipment'].search([('active', '=', True)])
#         for rec in self:
#             equipment = self.env["maintenance.equipment"].create({
#                 'name': rec.name,
#                 'name_of_equipment': rec.project_id and rec.project_id.name_of_equipment or False,
#                 'owner_user_id': rec.user_id.id,
#             })
#         return True


