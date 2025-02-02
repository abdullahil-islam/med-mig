# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz


class Repair(models.Model):
    _inherit = 'repair.order'
    _order = 'number desc'

    
    def _count_documents(self):
        for rec in self:
            document_ids = self.env['ir.attachment'].sudo().search([
                ('res_id', '=', rec.id), ('res_model', '=', 'repair.order')])
            rec.document_count = len(document_ids)

    
    def _compute_group(self):
        context = self.env.context
        for rec in self:
            if context.get('uid'):
                user = self.env['res.users'].browse(context.get('uid'))
                rec.is_engineer = False
                if user.has_group('repair_maintenance.group_maintenance_technician'):
                    rec.is_engineer = True
        return True

    @api.model
    def get_status(self):
        login_user = self.env.user
        admin_uid = self.env.ref('base.user_admin').id
        is_hospital_user = self.user_has_groups('repair_maintenance.group_maintenance_hospital_user')
        is_technician = self.user_has_groups('repair_maintenance.group_maintenance_technician')

        if is_hospital_user:
            return 'new_request'
        else:
            return 'draft'

    @api.model
    def _get_default_teamhead(self):
        teamhead = False
        context = self._context
        user = self.env['res.users'].browse(context.get('uid'))
        if user.has_group('repair_maintenance.group_maintenance_team_head'):
            teamhead = user.id
        return teamhead

    @api.model
    def _get_default_executives(self):
        executive_eng = False
        users = self.env['res.users'].sudo().search([])
        for user in users:
            if user.has_group('repair_maintenance.group_maintenance_executive') and user.login == 'paulpk@medionicsbd.com':
                executive_eng = user.id
        return executive_eng

    @api.model
    def get_technician(self):
        user = self.env['res.users'].sudo().browse(self._context.get('uid'))
        is_technician = user.has_group('repair_maintenance.group_maintenance_technician')
        res = False
        if is_technician:
            res = self.env.user
        return res
    
    @api.model
    def get_inloop(self):
        user = self.env['res.users'].sudo().browse(self._context.get('uid'))
        is_technician = user.has_group('repair_maintenance.group_maintenance_technician')
        res = False
        if is_technician:
            res = self.env.user
        return res

    
    def action_repair_start(self):
        """ Writes repair order state to 'Under Repair'
        @return: True
        """

        if self.filtered(lambda repair: repair.state not in ['confirmed', 'ready']):
            raise UserError(_("Repair must be confirmed before starting reparation."))
        self.mapped('operations').write({'state': 'confirmed'})
        self.write({'start_repair_date':fields.Datetime.now()})
        return self.write({'state': 'under_repair'})

    
    def action_repair_end(self):
        """ Writes repair order state to 'To be invoiced' if invoice method is
        After repair else state is set to 'Ready'.
        @return: True
        """
        end_repair = fields.Datetime.now()
        self.write({'end_repair_date': end_repair})
        now_timezone1 = pytz.UTC.localize(self.start_repair_date).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
        start_date = datetime.strptime(fields.Datetime.to_string(now_timezone1), "%Y-%m-%d %H:%M:%S")
        now_timezone = pytz.UTC.localize(self.end_repair_date).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
        end_date = datetime.strptime(fields.Datetime.to_string(now_timezone), "%Y-%m-%d %H:%M:%S")
        
        
        template_engineer = self.env.ref('repair_maintenance.new_repair_end_email_template').with_context(end_time=end_date, start_time=start_date).send_mail(self.id, force_send=True)
        if self.filtered(lambda repair: repair.state != 'under_repair'):
            raise UserError(_("Repair must be under repair in order to end reparation."))
        for repair in self:
            repair.write({'repaired': True})
            vals = {'state': 'done'}
            vals['move_id'] = repair.action_repair_done().get(repair.id)
            if not repair.invoiced and repair.invoice_method == 'after_repair':
                vals['state'] = '2binvoiced'
            repair.write(vals)

        return True

    @api.model
    def calculate_duration_of_repair(self):
        for rec in self:
            end_date = False
            if not rec.end_repair_date:
                end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:
                end_date = rec.end_repair_date

            diff_str = ''
            if rec.start_repair_date and end_date:
                from_date = datetime.strptime(str(rec.start_repair_date), '%Y-%m-%d %H:%M:%S')
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
            rec.duration_of_repair = diff_str

    number = fields.Integer("Number for sequence")
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
    technician_id = fields.Many2many('res.users', string='Responsible Engr', default=get_technician)
    inloop_ids = fields.Many2many('res.users','inloop_id','users_id','rel_inloop_users', string='Support Engr')
    team_head_id = fields.Many2one('res.users', string='Team Head', default=_get_default_teamhead)
    executive_engineer_id = fields.Many2one('res.users', string='EDE', default=_get_default_executives)
    scheduled_date = fields.Date('Scheduled Date')
    maintenance_team_id = fields.Many2one('maintenance.team', 'Assign Team')
    document_count = fields.Integer(compute='_count_documents',
                                    string='# Documents')
    is_new_request = fields.Boolean('New Request')
    is_engineer = fields.Boolean('Is Engineer', compute='_compute_group')
    # categ_id = fields.Many2one(
    #     'product.category', related='product_id.categ_id', string='Category of Product')
    categ_id = fields.Many2one('product.category', string='Category of Product')

    # Default field for rename label.
    product_id = fields.Many2one(
        'product.product', string='Machine',
        readonly=True, required=True, states={'draft': [('readonly', False)]})
    equipment_id = fields.Many2one('maintenance.equipment',related="product_id.equipment_id", string='Equipment')

    category_id = fields.Many2one('maintenance.equipment.category', string='Category')
    location = fields.Char('Used in location')
    tag_id = fields.Many2many('res.partner.category',related="partner_id.category_id", string="Tags")


    state = fields.Selection([
        ('new_request', 'New Request'),
        ('draft', 'Quotation'),
        ('cancel', 'Cancelled'),
        ('confirmed', 'Confirmed'),
        ('under_repair', 'Under Repair'),
        ('ready', 'Ready to Repair'),
        ('2binvoiced', 'To be Invoiced'),
        ('invoice_except', 'Invoice Exception'),
        ('done', 'Repaired')], string='Status',
        copy=False, default=get_status, readonly=True, track_visibility='onchange',
        help="* The \'Draft\' status is used when a user is encoding a new and unconfirmed repair order.\n"
             "* The \'Confirmed\' status is used when a user confirms the repair order.\n"
             "* The \'Ready to Repair\' status is used to start to repairing, user can start repairing only after repair order is confirmed.\n"
             "* The \'To be Invoiced\' status is used to generate the invoice before or after repairing done.\n"
             "* The \'Done\' status is set when repairing is completed.\n"
             "* The \'Cancelled\' status is used when user cancel repair order.")
    product_id = fields.Many2one(
        'product.product', string='Product to Repair',
        readonly=True, required=True, states={'new_request': [('readonly', False)], 'draft': [('readonly', False)]})
    operations = fields.One2many(
        'repair.line', 'repair_id', 'Parts',
        copy=True, readonly=True, states={'new_request': [('readonly', False)], 'draft': [('readonly', False)]})
    fees_lines = fields.One2many(
        'repair.fee', 'repair_id', 'Operations',
        copy=True, readonly=True, states={'new_request': [('readonly', False)], 'draft': [('readonly', False)]})
    invoice_method = fields.Selection([
        ("none", "No Invoice"),
        ("b4repair", "Before Repair")], string="Invoice Method",
        default='none', index=True, readonly=True, required=True,
        states={'draft': [('readonly', False)]},
        help='Selecting \'Before Repair\' or \'After Repair\' will allow you to generate invoice before or after the repair is done respectively. \'No invoice\' means you don\'t want to generate invoice for this repair order.')
    operations = fields.One2many(
        'repair.line', 'repair_id', 'Parts',
        copy=True, readonly=True, states={'draft': [('readonly', False)], 'confirmed': [('readonly', False)],
                                          'under_repair': [('readonly', False)]})
    fees_lines = fields.One2many(
        'repair.fee', 'repair_id', 'Operations',
        copy=True, readonly=True, states={'draft': [('readonly', False)], 'confirmed': [('readonly', False)],
                                          'under_repair': [('readonly', False)]})

    start_repair_date = fields.Datetime(string='Start Repair', readonly=True)
    end_repair_date = fields.Datetime(string='End Repair', readonly=True)
    duration_of_repair = fields.Char(string="Duration of Task", compute=calculate_duration_of_repair)


    @api.onchange('type')
    def onchange_equipment_type(self):
        if self.type and self.type == 'on_call':
            self.from_date = False
            self.to_date = False

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

    @api.onchange('product_id')
    def onchange_products(self):
        if self.product_id:
            equipment = self.product_id.sudo().equipment_id
            partner = equipment.partner_id or False
            if equipment:
                self.maintenance_team_id = equipment.maintenance_team_id and equipment.maintenance_team_id.id or False
                self.from_date = equipment.from_date or ''
                self.to_date = equipment.to_date or ''
                self.partner_id = equipment.partner_id and equipment.partner_id.id or False
                # self.technician_id = equipment.technician_user_id and equipment.technician_user_id.id or False
                self.street = partner and partner.street or ''
                self.street2 = partner and partner.street2 or ''
                self.zip = partner and partner.zip or ''
                self.city = partner and partner.city or ''
                self.state_id = partner and partner.state_id and partner.state_id.id or ''
                self.country_id = partner and partner.country_id and partner.country_id.id or ''
                self.phone = equipment.phone or ''
                self.type = equipment.type or ''
                self.maintenance_team_id = equipment.maintenance_team_id and equipment.maintenance_team_id.id or False
                self.from_date = equipment.from_date
                self.to_date = equipment.to_date
                self.categ_id = self.product_id.categ_id and self.product_id.categ_id.id or False
                self.category_id = equipment.category_id and equipment.category_id.id or False
                self.location = equipment.location or False




    
    def action_repair_request(self):
        users = self.env['res.users'].sudo().search([])
        template_rec = self.env.ref('repair_maintenance.repair_order_request_email_template')
        for user in users:
            if user.has_group('repair_maintenance.group_maintenance_executive'):
                partner_email = user.partner_id.email
                template_rec.send_mail(self.id, force_send=True, email_values={'email_to': partner_email})
        self.write({'state': 'draft', 'is_new_request': True})

    
    def document_view(self):
        self.ensure_one()
        action = self.env.ref('repair_maintenance.action_attachment_maintenance')
        context = dict(self._context)
        context.update({
            'default_res_id': self.id,
            'default_res_model': 'repair.order',
            'default_res_model_name': 'Repair Order',
            'tree_view_ref': 'repair_maintenance.view_attachment_tree_maintenance',
            'form_view_ref': 'repair_maintenance.view_attachment_form_maintenance'})
        result = {
            'name': action.name,
            'domain': [('res_id', '=', self.id), ('res_model', '=', 'repair.order')],
            'help': action.help,
            'type': action.type,
            'view_mode': action.view_mode,
            'target': action.target,
            'context': context,
            'res_model': action.res_model,
        }
        return result

    @api.model
    def create(self, vals):
        uid = self._context.get('uid')
        user = self.env['res.users'].sudo().browse(uid)
        hospital_user = user.has_group('repair_maintenance.group_maintenance_hospital_user')
        if hospital_user:
            vals.update({'partner_id': user.partner_id.id or False})
        ctx = self._context.copy()
        if ctx and 'default_name' in ctx:
            vals['name'] = self.env['ir.sequence'].next_by_code('repair.order')
        res = super(Repair, self).create(vals)
        if res.name:
            res.number = int(res.name.split("/")[-1])
        if res.maintenance_team_id and res.maintenance_team_id.member_ids:
            for line in res.maintenance_team_id.member_ids:
                exist = self.env['mail.followers'].sudo().search([('res_id','=', res.id),('partner_id','=', line.partner_id.id)])
                if not exist:
                    self.env['mail.followers'].sudo().create({
                    'res_id': res.id,
                    'res_model': 'repair.order',
                    'partner_id': line.partner_id.id,
                    })
        if res.inloop_ids:
            for line in res.inloop_ids:
                exist = self.env['mail.followers'].sudo().search([('res_id','=', res.id),('partner_id','=', line.partner_id.id)])
                if not exist:
                    self.env['mail.followers'].sudo().create({
                    'res_id': res.id,
                    'res_model': 'repair.order',
                    'partner_id': line.partner_id.id,
                    })
        return res

    
    def write(self, vals):
        for rec in self:
            if rec.state == 'done':
                raise ValidationError(_("You can't update order which is in the repaired stage!"))
        res = super(Repair, self).write(vals)
        if self.inloop_ids and vals and 'inloop_ids' in vals:
            for line in self.inloop_ids:
                self.env['mail.followers'].sudo().create({
                'res_id': self.id,
                'res_model': 'repair.order',
                'partner_id': line.partner_id.id,
                })
        return res

    def action_validate(self):
        self.ensure_one()
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        available_qty_owner = self.env['stock.quant']._get_available_quantity(self.product_id, self.location_id,
                                                                              self.lot_id, owner_id=self.partner_id,
                                                                              strict=True)
        available_qty_noown = self.env['stock.quant']._get_available_quantity(self.product_id, self.location_id,
                                                                              self.lot_id, strict=True)
        for available_qty in [available_qty_owner, available_qty_noown]:
            # if float_compare(available_qty, self.product_qty, precision_digits=precision) >= 0:
            return self.action_repair_confirm()
            # else:
            #    return {
            #        'name': _('Insufficient Quantity'),
            #        'view_type': 'form',
            #        'view_mode': 'form',
            #        'res_model': 'stock.warn.insufficient.qty.repair',
            #        'view_id': self.env.ref('repair.stock_warn_insufficient_qty_repair_form_view').id,
            #        'type': 'ir.actions.act_window',
            #        'context': {
            #            'default_product_id': self.product_id.id,
            #            'default_location_id': self.location_id.id,
            #            'default_repair_id': self.id
            #            },
            #        'target': 'new'
            #    }

    
    def action_mail_send(self):
        '''Send email to engineer and team head.'''
        template_engineer = self.env.ref('repair_maintenance.email_template_repair_order_engineer', False)
        template_teamhead = self.env.ref('repair_maintenance.email_template_repair_order_teamhead', False)
        teamhead_email = self.team_head_id and self.team_head_id.partner_id and self.team_head_id.partner_id.email or ''
        start_date = ''
        end_date = ''
        if self.start_repair_date:
            now_timezone1 = pytz.UTC.localize(self.start_repair_date).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
            start_date = datetime.strptime(fields.Datetime.to_string(now_timezone1), "%Y-%m-%d %H:%M:%S")
        if self.end_repair_date:
            now_timezone = pytz.UTC.localize(self.end_repair_date).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
            end_date = datetime.strptime(fields.Datetime.to_string(now_timezone), "%Y-%m-%d %H:%M:%S")
        
        if self.technician_id:
            template_engineer.with_context(end_time=end_date, start_time=start_date).send_mail(self.id, force_send=True,
                                        email_values={'email_to': ','.join(self.technician_id.mapped('email'))})
            template_teamhead.with_context(end_time=end_date, start_time=start_date).send_mail(self.id, force_send=True, email_values={'email_to': ','.join(self.inloop_ids.mapped('email'))})
        if teamhead_email:
            template_teamhead.with_context(end_time=end_date, start_time=start_date).send_mail(self.id, force_send=True, email_values={'email_to': teamhead_email})
            


        return True

    @api.model
    def _cron_repair_start(self):
        repair_start = self.search([('state', '=', 'under_repair')])
        # repair_start = self.search([('state', '=', 'under_repair'), ('start_repair_date', '<', fields.Date.to_string(fields.Datetime.today().date() + relativedelta(hours=24)))])
        for repair in repair_start:
            start_date = ''
            end_date = ''
            if repair.start_repair_date:
                now_timezone1 = pytz.UTC.localize(repair.start_repair_date).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
                start_date = datetime.strptime(fields.Datetime.to_string(now_timezone1), "%Y-%m-%d %H:%M:%S")
            if repair.end_repair_date:
                now_timezone = pytz.UTC.localize(repair.end_repair_date).astimezone(pytz.timezone(self.env.user.tz or 'UTC'))
                end_date = datetime.strptime(fields.Datetime.to_string(now_timezone), "%Y-%m-%d %H:%M:%S")
            self.env.ref('repair_maintenance.new_repair_star_email_template').with_context(end_time=end_date, start_time=start_date).send_mail(repair.id, force_send=True)

