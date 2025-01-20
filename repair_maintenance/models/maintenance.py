# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
import pytz




class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    name = fields.Char('Machine Name', required=False, translate=True)
    project_id = fields.Many2one('project.project', string="Project", domain="[('name_of_equipment', '=', name_of_equipment),('complete_project', '=', False)]")
    type = fields.Selection([('cmc', 'CMC'),
                             ('amc', 'AMC'),
                             ('warranty', 'Warranty'),
                             ('free_service', 'Free Service'),
                             ('on_call', 'On Call')], string="Service Type")
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    phone = fields.Char('Phone')
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    # Default field for rename label.
    partner_id = fields.Many2one('res.partner', string='Customer/Vendor Name', domain="['|',('customer_rank', '=', 1),('supplier_rank', '=', 1)]")
    maintenance_team_id = fields.Many2one('maintenance.team', string='Team')
    technician_user_id = fields.Many2one('res.users', string='Engineer', track_visibility='onchange', oldname='user_id')
    product_id = fields.Many2one('product.product', 'Product')
    category_id = fields.Many2one('maintenance.equipment.category', string='Machine Category',
                                  track_visibility='onchange', group_expand='_read_group_category_ids')
    name_of_equipment = fields.Selection(
        [('mri', 'MRI-'), ('ct', 'CT-'), ('xr', 'XR-'), ('usg', 'USG-'), ('cr', 'CR-'), ('fpd', 'FPD-'),
         ('mam', 'MAM-'),
         ('bmd', 'BMD-'), ('opg', 'OPG-'), ('crm', 'CRM-'), ('prt', 'PRT-'), ('omprt', 'PRTOM-')],
        string="Name Of Equipment")
    repair_order_ids = fields.One2many('repair.order','equipment_id')
    repair_count = fields.Integer(compute='_compute_repair_count', string="Repair Count", store=True)

    @api.depends('repair_order_ids')
    def _compute_repair_count(self):
        self.repair_count = len(self.repair_order_ids)

    @api.model
    def _cron_to_date_requests(self):
        call = self.search([('to_date', '<', fields.Datetime.now()), ('type', '!=', 'on_call')])
        for rec in call:
            if rec.to_date:
                rec.type = 'on_call'

    @api.model
    def _cron_to_date_service_status(self):
        maintenance_orders = self.search([('to_date', '=', fields.Date.to_string(fields.Datetime.now().date() + relativedelta(months=1)))])
        for oneorder in maintenance_orders:
            self.env.ref('repair_maintenance.email_template_machine_service_status').send_mail(oneorder.id, force_send=True)


    @api.model
    def _read_group_category_ids(self, categories, domain, order):
        """ Read group customization in order to display all the categories in
            the kanban view, even if they are empty.
        """
        category_ids = categories._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return categories.browse(category_ids)

    @api.onchange('type')
    def onchange_equipment_type(self):
        if self.type and self.type == 'on_call':
            self.from_date = False
            self.to_date = False
            
    @api.onchange('project_id')
    def onchange_project(self):
        if self.project_id:
            self.name = self.project_id.name.split(",")[0]

    @api.onchange('partner_id')
    def onchange_partner(self):
        if self.partner_id:
            self.street = self.partner_id.street
            self.street2 = self.partner_id.street2
            self.zip = self.partner_id.zip
            self.city = self.partner_id.city
            self.state_id = self.partner_id.state_id and self.partner_id.state_id.id or ''
            self.country_id = self.partner_id.country_id and self.partner_id.country_id.id or ''
            self.phone = self.partner_id.phone

    # @api.constrains('name')
    # def _check_name_of_equipment(self):
    #     if self.name:
    #         equipments = self.search([('id', '!=', self.id), ('name', '=', self.name)])
    #         if equipments:
    #             raise ValidationError(_('Equipment name must be unique!'))

    @api.model
    def create(self, vals):
#         if vals.get('name_of_equipment') == 'mri':
#             vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.mri')
#         if vals.get('name_of_equipment') == 'ct':
#             vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.ct')
#         if vals.get('name_of_equipment') == 'xr':
#             vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.xr')
#         if vals.get('name_of_equipment') == 'usg':
#             vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.usg')
#         if vals.get('name_of_equipment') == 'cr':
#             vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.cr')
#         if vals.get('name_of_equipment') == 'fpd':
#             vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.fpd')
#         if vals.get('name_of_equipment') == 'mam':
#             vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.mam')
#         if vals.get('name_of_equipment') == 'bmd':
#             vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.bmd')
#         if vals.get('name_of_equipment') == 'opg':
#             vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.opg')
#         if vals.get('name_of_equipment') == 'crm':
#             vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.crm')
#         if vals.get('name_of_equipment') == 'prt':
#             vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.prt')
#         if vals.get('name_of_equipment') == 'omprt':
#             vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.omprt')
        result = super(MaintenanceEquipment, self).create(vals)
        categ_id = self.env.ref('product.product_category_all').id
        cat = self.env['product.category'].search([('name','=', 'Equipment Product')],limit=1)
        if cat:
            categ_id = cat.id
        product = self.env['product.product'].create({
            'name': result.project_id.name.split(",")[0] or False,
            'default_code': vals.get('serial_no'),
            'type': 'product',
            'categ_id': categ_id,
            'is_equipment': True,
            'sale_ok': True,
            'purchase_ok': True,
            'equipment_id': result.id})
        result.product_id = product and product.id or False
        result.name = result.project_id.name.split(",")[0]
        if result.project_id:
            result.project_id.write({'complete_project':True})
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        context = self._context
        if context and context.get('machine_based_on_partner', False):
            equipment_ids = self.env['maintenance.equipment'].search(
                [('partner_id', '=', context.get('machine_based_on_partner'))])
            args += [('id', 'in', equipment_ids.ids)]
        return super(MaintenanceEquipment, self).name_search(
            name=name, args=args, operator=operator, limit=limit)


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    
    def _count_documents(self):
        for rec in self:
            document_ids = self.env['ir.attachment'].sudo().search([
                ('res_id', '=', rec.id), ('res_model', '=', 'maintenance.request')])
            rec.document_count = len(document_ids)

    
    def _compute_group(self):
        context = self.env.context
        if context.get('uid'):
            user = self.env['res.users'].browse(context.get('uid'))
            self.is_engineer = False
            if user.has_group('repair_maintenance.group_maintenance_technician'):
                self.is_engineer = True
        return True
    
    @api.model
    def _get_default_executives(self):
        executive_eng = False
        users = self.env['res.users'].sudo().search([])
        for user in users:
            if user.has_group('repair_maintenance.group_maintenance_executive') and user.login == 'paulpk@medionicsbd.com':
                executive_eng = user.id
        return executive_eng

    type = fields.Selection([('cmc', 'CMC'),
                             ('amc', 'AMC'),
                             ('warranty', 'Warranty'),
                             ('free_service', 'Free Service'),
                             ('on_call', 'On Call')], string="Service Type")
    name = fields.Char('Subjects', default=lambda self: self.env['ir.sequence'].next_by_code('maintenance.request'), required=False)
    schedule_date = fields.Date('Scheduled Date',
                                help="Date the maintenance team plans the maintenance.  It should not differ much from the Request Date. ")
    partner_id = fields.Many2one('res.partner', string='Customer', ondelete='restrict')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    phone = fields.Char('Phone')
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    reminder_time = fields.Date('Reminder Time')
    parts_reference = fields.Char(string='Service/Spare Parts Reference')
    document_count = fields.Integer(compute='_count_documents',
                                    string='# Documents')
    is_permanent = fields.Boolean('Is Permanent', copy=False)
    team_head_id = fields.Many2one('res.users', string='Team Head', default=lambda self: self.env.user.id or False)
    executive_engineer_id = fields.Many2one('res.users', string='EDE', default=_get_default_executives)
    equipment_id = fields.Many2one('maintenance.equipment', string='Machine',
                                   ondelete='restrict', index=True)
    is_engineer = fields.Boolean('Is Engineer', compute='_compute_group')
    cat_id = fields.Many2one('repair.order', string='Category')

    user_ids = fields.Many2many('res.users', string="Responsible Engr")
    tag_id = fields.Many2many('res.partner.category',related="partner_id.category_id", string="Tags")
    
    
    @api.model
    def create(self, vals):
        ctx = self._context.copy()
        if ctx and 'default_name' in ctx:
            vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.request')
        res = super(MaintenanceRequest, self).create(vals)
        if res.maintenance_team_id and res.maintenance_team_id.member_ids:
            for line in res.maintenance_team_id.member_ids:
                exist = self.env['mail.followers'].sudo().search([('res_id','=', res.id),('partner_id','=', line.partner_id.id)])
                if not exist:
                    self.env['mail.followers'].sudo().create({
                    'res_id': res.id,
                    'res_model': 'maintenance.request',
                    'partner_id': line.partner_id.id,
                    })
        return res

    
    def action_star_maintenance(self):
        for rec in self:
            self.write({'x_maintenance_start_date': fields.Datetime.now()})
            # self.env.ref('repair_maintenance.new_equipment_email_template').send_mail(rec.id, force_send=True)

    
    def action_end_maintenance(self):
        for rec in self:
            stage = self.env['maintenance.stage'].search([('name','=','Permanent')])
            wri_dict = {}
            if stage:
                wri_dict = {'stage_id': stage.id, 'x_maintenance_end_date': fields.Datetime.now()}
            else:
                wri_dict = {'x_maintenance_end_date': fields.Datetime.now()}
            self.write(wri_dict)
            # self.env.ref('repair_maintenance.new_equipment_email_template').send_mail(rec.id, force_send=True)

    
    def calculate_duration_of_task(self):
        for rec in self:
            end_date = False
            if not rec.x_maintenance_end_date:
                end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:
                end_date = rec.x_maintenance_end_date
            if rec.x_maintenance_start_date and end_date:
                from_date = datetime.strptime(str(rec.x_maintenance_start_date), '%Y-%m-%d %H:%M:%S')
                to_date = datetime.strptime(str(end_date), '%Y-%m-%d %H:%M:%S')
                diff_str = ''
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

    x_maintenance_start_date = fields.Datetime(string="Start Date")
    x_maintenance_end_date = fields.Datetime(string="End Date")
    duration_of_task = fields.Char(string="Duration of Task", compute=calculate_duration_of_task)

    @api.model
    def _cron_team_head(self):
        team_head = self.search(
            [('schedule_date', '=', fields.Date.to_string(fields.Datetime.today().date() + relativedelta(days=60)))])
        for order in team_head:
            if order.team_head_id:
                self.env.ref('repair_maintenance.team_head_email_template').send_mail(order.id, force_send=True)
            if order.user_ids:
                self.env.ref('repair_maintenance.responsible_email_template').send_mail(order.id, force_send=True, email_values={'email_to': ','.join(self.user_ids.mapped('email'))})

    # @api.model
    # def create(self, vals):
    #     vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.request')
    #     return super(MaintenanceRequest, self).create(vals)


    @api.onchange('type')
    def onchange_equipment_type(self):
        if self.type and self.type == 'on_call':
            self.from_date = False
            self.to_date = False

    @api.onchange('equipment_id')
    def onchange_equipments(self):
        if self.equipment_id:
            self.partner_id = self.equipment_id.partner_id and self.equipment_id.partner_id.id or False
            self.phone = self.equipment_id.phone or ''
            self.type = self.equipment_id.type or ''
            self.maintenance_team_id = self.equipment_id.maintenance_team_id and self.equipment_id.maintenance_team_id.id or False
            self.from_date = self.equipment_id.from_date
            self.to_date = self.equipment_id.to_date

    @api.onchange('partner_id')
    def onchange_partner(self):
        if self.partner_id:
            self.street = self.partner_id.street
            self.street2 = self.partner_id.street2
            self.zip = self.partner_id.zip
            self.city = self.partner_id.city
            self.state_id = self.partner_id.state_id and self.partner_id.state_id.id or ''
            self.country_id = self.partner_id.country_id and self.partner_id.country_id.id or ''

    
    def document_view(self):
        self.ensure_one()
        action = self.env.ref('repair_maintenance.action_attachment_maintenance')
        context = dict(self._context)
        context.update({
            'default_res_id': self.id,
            'default_res_model': 'maintenance.request',
            'default_res_model_name': 'Maintenance Request',
            'tree_view_ref': 'repair_maintenance.view_attachment_tree_maintenance',
            'form_view_ref': 'repair_maintenance.view_attachment_form_maintenance'})
        result = {
            'name': action.name,
            'domain': [('res_id', '=', self.id), ('res_model', '=', 'maintenance.request')],
            'help': action.help,
            'type': action.type,
            'view_mode': action.view_mode,
            'target': action.target,
            'context': context,
            'res_model': action.res_model,
        }
        return result
    
    def activity_update(self):
        """ Update maintenance activities based on current record set state.
        It reschedule, unlink or create maintenance request activities. """
        self.filtered(lambda request: not request.schedule_date).activity_unlink(['maintenance.mail_act_maintenance_request'])
        for request in self.filtered(lambda request: request.schedule_date):
            date_dl = fields.Datetime.from_string(request.schedule_date).date()
            assign_user = False
            if request.user_ids:
                assign_user = request.user_ids.ids[0]
            else:
                assign_user = request.owner_user_id.id or self.env.uid
            updated = request.activity_reschedule(
                ['maintenance.mail_act_maintenance_request'],
                date_deadline=date_dl,
                new_user_id=assign_user)
            if not updated:
                if request.equipment_id:
                    note = _('Request planned for <a href="#" data-oe-model="%s" data-oe-id="%s">%s</a>') % (
                        request.equipment_id._name, request.equipment_id.id, request.equipment_id.display_name)
                else:
                    note = False
                request.activity_schedule(
                    'maintenance.mail_act_maintenance_request',
                    fields.Datetime.from_string(request.schedule_date).date(),
                    note=note, user_id=assign_user)


    
    def write(self, vals):
        context = self._context
        user = self.env['res.users'].browse(context.get('uid'))
        for rec in self:
            # engineer = user.has_group('repair_maintenance.group_maintenance_technician')
            # team_head = user.has_group('repair_maintenance.group_maintenance_team_head')
            # if vals.get('stage_id') and (engineer or team_head):
            #    raise ValidationError(_("You cannot move to the next stage \n Please contact to executive of engineering Head!"))

            prev_stage_rec = rec.stage_id.name
            stage_rec = self.env['maintenance.stage'].sudo().browse(vals.get('stage_id'))
            if prev_stage_rec == 'Permanent' and stage_rec.name != 'Permanent' and not vals.get('close_date'):
                raise ValidationError(_("You cannot modify permanent stage maintenance request!"))
        return super(MaintenanceRequest, self).write(vals)

    
    def _notify_teamhead_executive(self):
        '''Reminder to Team Head & Engineer to every day.'''
        today_date = datetime.now().date()
        maintenance_orders = self.env['maintenance.request'].sudo().search([('reminder_time', '=', today_date)])
        engineer_template = self.env.ref('repair_maintenance.maintenance_request_engineer_email_template')
        teamhead_template = self.env.ref('repair_maintenance.maintenance_request_teamhead_email_template')
        executive_template = self.env.ref('repair_maintenance.maintenance_request_executive_email_template')
        for maintenance in maintenance_orders:
            if maintenance.user_ids:
                # partner_email = maintenance.user_id.partner_id.email
                engineer_template.send_mail(maintenance.id, force_send=True, email_values={'email_to': ','.join(self.user_ids.mapped('email'))})

            if maintenance.team_head_id:
                partner_email = maintenance.team_head_id.partner_id.email
                teamhead_template.send_mail(maintenance.id, force_send=True, email_values={'email_to': partner_email})

            if maintenance.executive_engineer_id:
                partner_email = maintenance.executive_engineer_id.partner_id.email
                executive_template.send_mail(maintenance.id, force_send=True, email_values={'email_to': partner_email})
        return True

    
    def action_send_mail(self):
        template_engineer = self.env.ref('repair_maintenance.email_template_maintenance_request_engineer', False)
        template_teamhead = self.env.ref('repair_maintenance.email_template_maintenance_request_teamhead', False)
        teamhead_email = self.team_head_id and self.team_head_id.partner_id and self.team_head_id.partner_id.email or ''
        
        
        start_date = ''
        end_date = ''
        if self.x_maintenance_start_date:
            now_timezone1 = pytz.UTC.localize(self.x_maintenance_start_date).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
            start_date = datetime.strptime(fields.Datetime.to_string(now_timezone1), "%Y-%m-%d %H:%M:%S")
        if self.x_maintenance_end_date:
            now_timezone = pytz.UTC.localize(self.x_maintenance_end_date).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
            end_date = datetime.strptime(fields.Datetime.to_string(now_timezone), "%Y-%m-%d %H:%M:%S")
        
        
        if self.user_ids:
            template_engineer.with_context(end_time=end_date, start_time=start_date).send_mail(self.id, force_send=True,
                                        email_values={'email_to': ','.join(self.user_ids.mapped('email'))})
        if teamhead_email:
            template_teamhead.with_context(end_time=end_date, start_time=start_date).send_mail(self.id, force_send=True, email_values={'email_to': teamhead_email})
        return True


