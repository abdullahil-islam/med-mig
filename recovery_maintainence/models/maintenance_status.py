from unicodedata import category

from odoo import models, fields, api, _
from odoo.addons.test_impex.models import field
from odoo.exceptions import ValidationError, UserError
from odoo.tools import datetime
import logging

_logger = logging.getLogger(__name__)


class MaintenanceStatus(models.Model):
    _name = 'maintenance.status'
    _description = 'Maintenance Status'

    name = fields.Char(string='Name', readonly=True, required=True, default='New')
    description = fields.Text(string='Description')
    status_date = fields.Date(string='Date')
    partner_id = fields.Many2one('res.partner', string='Partner')
    partner_full_address = fields.Char(string='Partner Address', compute='compute_partner_full_address', store=True)
    contact_address = fields.Char(string='Contact Address')
    partner_email = fields.Char(string='Partner Email')
    total_amount = fields.Float(string='Total Amount', compute='compute_totals')
    total_receive_amount = fields.Float(string='Total Receive Amount', compute='compute_totals')
    balance_amount = fields.Float(string='Balance Amount', compute='compute_totals')
    equipment_ids = fields.Many2many('maintenance.equipment', string='Machine Name', domain="[('partner_id', '=', partner_id), ('type', '!=', 'on_call')]")
    equipment_model_ids = fields.Many2many('maintenance.equipment.category', string='Machine Model', compute='compute_equipment_models')
    # installment_date = fields.Date(string='Installation Date', related='equipment_id.effective_date')
    # type = fields.Selection([
    #     ('cmc', 'CMC'),
    #     ('amc', 'AMC'),
    #     ('warranty', 'Warranty'),
    #     ('free_service', 'Free Service'),
    #     ('on_call', 'On Call')
    # ], string="Service Type", related='equipment_id.type')
    remarks = fields.Text()
    billing_period = fields.Char(compute='compute_billing_period')
    # product_ids = fields.Many2many('product.product', string='Products')
    maintenance_line_ids = fields.One2many('maintenance.status.line', 'maintenance_status_id',
                                           string='Maintenance Lines')

    @api.depends('maintenance_line_ids', 'maintenance_line_ids.billing_amount', 'maintenance_line_ids.paid_amount', 'maintenance_line_ids.balance_due')
    def compute_totals(self):
        for rec in self:
            rec.total_amount = sum(rec.maintenance_line_ids.mapped('billing_amount'))
            rec.total_receive_amount = sum(rec.maintenance_line_ids.mapped('paid_amount'))
            rec.balance_amount = sum(rec.maintenance_line_ids.mapped('balance_due'))

    @api.depends('equipment_ids')
    def compute_equipment_models(self):
        for rec in self:
            rec.equipment_model_ids.unlink()
            rec.equipment_model_ids = [(4, equipment.category_id.id) for equipment in rec.equipment_ids if equipment.category_id]

    @api.depends('maintenance_line_ids', 'maintenance_line_ids.start_date', 'maintenance_line_ids.end_date')
    def compute_billing_period(self):
        for record in self:
            if record.maintenance_line_ids:
                start_period = min(record.maintenance_line_ids.mapped('start_date'))
                end_period = max(record.maintenance_line_ids.mapped('end_date'))
                billing_period = start_period.strftime("%B %d") if start_period else ''
                billing_period += ' to ' + end_period.strftime("%B %d") if end_period else ''
                record.billing_period = billing_period
            else:
                record.billing_period = ''

    @api.depends('partner_id')
    def compute_partner_full_address(self):
        for record in self:
            if record.partner_id:
                record.partner_full_address = record.name or '' + ', ' + record.partner_id.street or '' + ', ' + record.partner_id.city or '' + ', ' + record.partner_id.country_id.name or ''
            else:
                record.partner_full_address = ''

    @api.model
    def create(self, values):
        if values.get('name', _('New')) == 'New':
            values['name'] = self.env['ir.sequence'].next_by_code('maintenance.status.seq')
        return super(MaintenanceStatus, self).create(values)

    # def action_generate_invoice(self):
    #     invoice_lines = []
    #     for line in self.maintenance_line_ids:
    #         product = self.env.ref('recovery_maintainence.product_template_sb_type_{}'.format(line.sb_type))
    #         if not product:
    #             product = self.env['product.template'].search([('sb_type', '=', line.sb_type)], limit=1)
    #         if not product:
    #             raise ValidationError('Please make sure there is a service product exist of SB Type = {}.'.format(line.sb_type.upper()))
    #
    #         if product.property_account_expense_id:
    #             account_id = product.property_account_income_id
    #         elif product.categ_id.property_account_income_categ_id:
    #             account_id = product.categ_id.property_account_income_categ_id
    #         else:
    #             raise ValidationError('Please define income account in product or category of the product.')
    #         invoice_lines.append((0, 0, {
    #             'name': product.name,
    #             'product_id': product.product_variant_id.id,
    #             'quantity': 1,
    #             'price_unit': line.paid_amount,
    #             'account_id': account_id.id,
    #         }))
    #     invoice_val = {
    #         'name': 'Invoice For {}'.format(self.name),
    #         'partner_id': self.partner_id.id,
    #         'type': 'out_invoice',
    #         'journal_type': 'sale',
    #         'date_invoice': fields.Datetime.today().date(),
    #         'reference': self.name,
    #         'invoice_line_ids': invoice_lines,
    #         'is_from_maintenance': True,
    #     }
    #     try:
    #         invoice = self.env['account.invoice'].create(invoice_val)
    #         if invoice:
    #             self.invoice_id = invoice.id
    #     except Exception as e:
    #         _logger.error('Invoice cannot be created for some reason. {}'.format(e))
    #         raise UserError('Invoice cannot be created for some reason.')
    #
    # def open_related_invoice(self):
    #     if self.invoice_id:
    #         form_view = self.env.ref('account.invoice_form')
    #         return {
    #             'name': _('Invoice'),
    #             'res_model': 'account.invoice',
    #             'res_id': self.invoice_id.id,
    #             'views': [(form_view.id, 'form'),],
    #             'type': 'ir.actions.act_window',
    #             'target': 'current',
    #         }


class MaintenanceStatusLine(models.Model):
    _name = 'maintenance.status.line'

    name = fields.Char(string='Name', readonly=True, required=True, default='New')
    maintenance_status_id = fields.Many2one('maintenance.status', string='Maintenance Status')
    equipment_ids_dom = fields.Many2many('maintenance.equipment', string='Machine Name', related='maintenance_status_id.equipment_ids')
    partner_id = fields.Many2one('res.partner', string='Partner', related='maintenance_status_id.partner_id')
    billing_period = fields.Char(string='Billing Period', compute='compute_billing_period')
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    line_equipment_ids = fields.Many2many('maintenance.equipment', relation='maintenance_line_equipment_rel', string='Machine', domain="[('id', 'in', equipment_ids_dom)]", required=True)
    # equipment_id = fields.Many2one('maintenance.equipment', string='Machine', domain="[('id', 'in', equipment_ids)]", required=True)
    billing_date = fields.Date(string='Billing Date', required=True)
    billing_amount = fields.Float(string='Billing Amount')
    paid_date = fields.Date(string='Paid Date')
    paid_amount = fields.Float(string='Paid Amount', compute='compute_paid_amount')
    # invoiced_amount = fields.Float(string='Invoced Amount', compute='compute_invoiced_amount')
    vat_ait = fields.Float(string='Paid Amount')
    mrn_no = fields.Char(string='MRN No')
    balance_due = fields.Float(string='Balance Amount', compute='compute_balance_due', store=True)
    remarks = fields.Text(string='Remarks')
    sb_type = fields.Selection([
        ('amc', 'AMC'),
        ('call', 'On Call'),
        ('repair', 'Repair'),
    ], default='amc', required=True)
    attachment = fields.Binary(attachment=True)
    invoice_id = fields.Many2one('account.move', string='Billing Number')
    invoice_number = fields.Char(related='invoice_id.name')
    invoice_state = fields.Selection([
            ('draft','Draft'),
            ('open', 'Open'),
            ('in_payment', 'In Payment'),
            ('paid', 'Paid'),
            ('cancel', 'Cancelled'),
        ], related='invoice_id.state')
    is_locked = fields.Boolean(default=False)

    def action_lock_line(self):
        if self.is_locked and not self.user_has_groups('recovery_maintainence.group_maintenance_entry_manager'):
            raise ValidationError('You are not allowed to unlock this entry.')
        self.is_locked = not self.is_locked

    # invoice_ids = fields.One2many('account.invoice', 'maintenance_status_line_id')
    # allow_generate_invoice = fields.Boolean(compute='compute_allow_generate_invoice', store=True)

    # @api.depends('paid_amount', 'invoiced_amount')
    # def compute_allow_generate_invoice(self):
    #     for rec in self:
    #         rec.allow_generate_invoice = True if rec.paid_amount - rec.invoiced_amount > 0 else False

    # @api.depends('invoice_ids')
    # def compute_invoiced_amount(self):
    #     for rec in self:
    #         rec.invoiced_amount = sum(rec.invoice_ids.filtered(lambda x: x.state != 'cancel').mapped('amount_total'))

    @api.depends('invoice_id', 'invoice_id.amount_residual', 'billing_amount')
    def compute_balance_due(self):
        for rec in self:
            rec.balance_due = rec.invoice_id.amount_residual if rec.invoice_id else rec.billing_amount

    @api.depends('billing_amount', 'balance_due')
    def compute_paid_amount(self):
        for rec in self:
            rec.paid_amount = rec.billing_amount - rec.balance_due

    @api.model
    def create(self, values):
        if values.get('name', _('New')) == 'New' and values.get('sb_type', '') == 'amc':
            values['name'] = self.env['ir.sequence'].next_by_code('maintenance.line.amc.seq')
        elif values.get('name', _('New')) == 'New' and values.get('sb_type', '') == 'call':
            values['name'] = self.env['ir.sequence'].next_by_code('maintenance.line.oc.seq')
        elif values.get('name', _('New')) == 'New' and values.get('sb_type', '') == 'repair':
            values['name'] = self.env['ir.sequence'].next_by_code('maintenance.line.r.seq')
        return super(MaintenanceStatusLine, self).create(values)

    @api.depends('start_date', 'end_date')
    def compute_billing_period(self):
        for record in self:
            start_date = datetime.strftime(record.start_date, "%B %d") if record.start_date else ''
            end_date = datetime.strftime(record.end_date, "%B %d") if record.end_date else ''
            record.billing_period = start_date + ' to ' + end_date if start_date and end_date else ''

    def action_generate_invoice(self):
        invoice_lines = []
        for line in self:
            if line.billing_amount <= 0:
                raise ValidationError('There is nothing to invoice.')
            product = self.env.ref('recovery_maintainence.product_template_sb_type_{}'.format(line.sb_type))
            if not product:
                product = self.env['product.template'].search([('sb_type', '=', line.sb_type)], limit=1)
            if not product:
                raise ValidationError('Please make sure there is a service product exist of SB Type = {}.'.format(line.sb_type.upper()))

            if product.property_account_expense_id:
                account_id = product.property_account_income_id
            elif product.categ_id.property_account_income_categ_id:
                account_id = product.categ_id.property_account_income_categ_id
            else:
                raise ValidationError('Please define income account in product or category of the product.')
            invoice_lines.append((0, 0, {
                'name': product.name,
                'product_id': product.product_variant_id.id,
                'quantity': 1,
                'price_unit': line.billing_amount,
                'account_id': account_id.id,
                'tax_ids': False
            }))
        invoice_val = {
            'partner_id': self.maintenance_status_id.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_date': fields.Datetime.today().date(),
            'ref': f'{self.maintenance_status_id.name} - {self.name}',
            'invoice_line_ids': invoice_lines,
            'is_from_maintenance': True,
            'maintenance_status_line_id': self.id
        }
        try:
            invoice = self.env['account.move'].create(invoice_val)
            if invoice:
                self.invoice_id = invoice.id
        except Exception as e:
            _logger.error('Invoice cannot be created for some reason. {}'.format(e))
            raise UserError('Invoice cannot be created for some reason.')

    def open_related_invoices(self):
        if self.invoice_ids:
            form_view = self.env.ref('account.view_move_form')
            list_view = self.env.ref('account.view_out_invoice_tree')
            return {
                'name': _('Invoice'),
                'res_model': 'account.move',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', self.invoice_ids.ids)],
                'views': [(list_view.id, 'tree'), (form_view.id, 'form')],
                'type': 'ir.actions.act_window',
                'target': 'current',
            }

    def open_related_payments(self):
        if self.invoice_id.invoice_payments_widget:
            form_view = self.env.ref('account.view_account_payment_form')
            list_view = self.env.ref('account.view_account_payment_tree')
            payment_ids = []
            payment_widget = self.invoice_id.invoice_payments_widget.get('content', False)
            if payment_widget:
                payment_ids = [widget.get('account_payment_id') for widget in payment_widget]

            return {
                'name': _('Payments'),
                'res_model': 'account.payment',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', payment_ids)],
                'views': [(list_view.id, 'tree'), (form_view.id, 'form')],
                'type': 'ir.actions.act_window',
                'target': 'current',
            }
        else:
            raise ValidationError('There are currently no payment for this entry.')
