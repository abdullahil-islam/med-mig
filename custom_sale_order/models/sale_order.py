# -*- coding: utf-8 -*-
import json
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def _display_approve_button(self):
        for rec in self:
            if rec.approval_ids:
                rec.display_validate_button = False
            else:
                rec.display_validate_button = True
            hierarchy_last_approver = ''
            if rec.hierarchy_last_approver_id:
                hierarchy_last_approver += "Last Approved by : " + str(rec.hierarchy_last_approver_id.name)
                if rec.approval_ids:
                    rec.display_validate_button = False
                    hierarchy_last_approver += " <br/>Waiting approval from: "
                    for one_approval in rec.approval_ids:
                        hierarchy_last_approver += str(one_approval.name) + ", "
                else:
                    rec.display_validate_button = True
            rec.hierarchy_last_approver = hierarchy_last_approver
            rec.hierarchy_approval_pending = False
            if rec.state == 'draft' and self.env.user.id in rec.sudo().approval_ids.ids:
                rec.hierarchy_approval_pending = True

    quotation_template_ids = fields.Many2many(
        'sale.order.template',
        string="Quotation Templates"
    )

    approval_ids = fields.Many2many('res.users')
    hierarchy_last_approver_id = fields.Many2one('res.users')
    hierarchy_approval_seq = fields.Integer("Approval Sequence")
    hierarchy_approval_pending = fields.Boolean('Approval Pending', compute='_display_approve_button')
    hierarchy_last_approver = fields.Html(string='Last Approval', compute='_display_approve_button')
    display_validate_button = fields.Boolean('Display Validate Button', compute='_display_approve_button')

    bp_amount = fields.Monetary(currency_field='currency_id')
    bp_comment = fields.Char()
    other_exp1_amount = fields.Monetary(currency_field='currency_id')
    other_exp1_comment = fields.Char()
    other_exp2_amount = fields.Monetary(currency_field='currency_id')
    other_exp2_comment = fields.Char()
    total_exp_amount = fields.Monetary(currency_field='currency_id', compute='compute_total_expt_amount', store=True)

    cash_price_amount = fields.Monetary(currency_field='currency_id')
    so_advance_amount = fields.Monetary(currency_field='currency_id')
    so_balance_amount = fields.Monetary(currency_field='currency_id', compute='compute_so_balance_amount', store=True)
    down_payment_amount = fields.Monetary(currency_field='currency_id')
    down_payment_type = fields.Selection([('accounts', 'Accounts'), ('recovery', 'Recovery')],
                                         string='Down Payment Received By', track_visibility='always')
    remaining_amount = fields.Monetary(currency_field='currency_id', compute='compute_res_amount', store=True)
    phase1_installment_no = fields.Integer(default=1)
    phase1_each_installment = fields.Monetary(currency_field='currency_id')

    is_readonly_phase2 = fields.Boolean(compute='compute_readonly_phase2', store=True)
    phase2_init_installment_no = fields.Integer(compute='compute_readonly_phase2', store=True)
    phase2_installment_no = fields.Integer()
    phase2_each_installment = fields.Monetary(currency_field='currency_id')

    last_installment_amount = fields.Float(compute='compute_last_installments', store=True)

    instruction = fields.Text()
    month_of_warranty = fields.Integer()
    month_of_service_warranty = fields.Integer()

    tmp1_name = fields.Char(compute='_compute_checkpoint_data')
    tmp1_cash_price = fields.Float(compute='_compute_checkpoint_data')
    tmp1_policy_price = fields.Float(compute='_compute_checkpoint_data')
    tmp1_down_payment = fields.Float(compute='_compute_checkpoint_data')
    tmp1_no_of_installment = fields.Integer(compute='_compute_checkpoint_data')
    tmp1_warranty = fields.Integer(compute='_compute_checkpoint_data')
    tmp1_ups = fields.Char(compute='_compute_checkpoint_data')
    tmp1_transportation = fields.Char(compute='_compute_checkpoint_data')
    tmp1_any_other = fields.Char(compute='_compute_checkpoint_data')
    tmp1_cash_price_sheet = fields.Monetary(currency_field='currency_id')
    tmp1_amount_total = fields.Monetary(currency_field='currency_id')
    tmp1_down_payment_sheet = fields.Monetary(currency_field='currency_id')
    tmp1_advance_payment = fields.Monetary(currency_field='currency_id')
    tmp1_balance_amount = fields.Monetary(currency_field='currency_id')
    tmp1_warranty_month = fields.Integer()
    tmp1_installment_no = fields.Integer()
    tmp1_green_cash_price = fields.Boolean(compute='compute_tmp1_approval_colors', store=True)
    tmp1_green_price = fields.Boolean(compute='compute_tmp1_approval_colors', store=True)
    tmp1_green_downpaymet = fields.Boolean(compute='compute_tmp1_approval_colors', store=True)
    tmp1_green_installment = fields.Boolean(compute='compute_tmp1_approval_colors', store=True)
    tmp1_green_warranty = fields.Boolean(compute='compute_tmp1_approval_colors', store=True)

    tmp2_name = fields.Char(compute='_compute_checkpoint_data')
    tmp2_cash_price = fields.Float(compute='_compute_checkpoint_data')
    tmp2_policy_price = fields.Float(compute='_compute_checkpoint_data')
    tmp2_down_payment = fields.Float(compute='_compute_checkpoint_data')
    tmp2_no_of_installment = fields.Integer(compute='_compute_checkpoint_data')
    tmp2_warranty = fields.Integer(compute='_compute_checkpoint_data')
    tmp2_ups = fields.Char(compute='_compute_checkpoint_data')
    tmp2_transportation = fields.Char(compute='_compute_checkpoint_data')
    tmp2_any_other = fields.Char(compute='_compute_checkpoint_data')
    tmp2_cash_price_sheet = fields.Monetary(currency_field='currency_id')
    tmp2_amount_total = fields.Monetary(currency_field='currency_id')
    tmp2_down_payment_sheet = fields.Monetary(currency_field='currency_id')
    tmp2_advance_payment = fields.Monetary(currency_field='currency_id')
    tmp2_balance_amount = fields.Monetary(currency_field='currency_id')
    tmp2_warranty_month = fields.Integer()
    tmp2_installment_no = fields.Integer()
    tmp2_green_cash_price = fields.Boolean(compute='compute_tmp2_approval_colors', store=True)
    tmp2_green_price = fields.Boolean(compute='compute_tmp2_approval_colors', store=True)
    tmp2_green_downpaymet = fields.Boolean(compute='compute_tmp2_approval_colors', store=True)
    tmp2_green_installment = fields.Boolean(compute='compute_tmp2_approval_colors', store=True)
    tmp2_green_warranty = fields.Boolean(compute='compute_tmp2_approval_colors', store=True)

    tmp3_name = fields.Char(compute='_compute_checkpoint_data')
    tmp3_cash_price = fields.Float(compute='_compute_checkpoint_data')
    tmp3_policy_price = fields.Float(compute='_compute_checkpoint_data')
    tmp3_down_payment = fields.Float(compute='_compute_checkpoint_data')
    tmp3_no_of_installment = fields.Integer(compute='_compute_checkpoint_data')
    tmp3_warranty = fields.Integer(compute='_compute_checkpoint_data')
    tmp3_ups = fields.Char(compute='_compute_checkpoint_data')
    tmp3_transportation = fields.Char(compute='_compute_checkpoint_data')
    tmp3_any_other = fields.Char(compute='_compute_checkpoint_data')
    tmp3_cash_price_sheet = fields.Monetary(currency_field='currency_id')
    tmp3_amount_total = fields.Monetary(currency_field='currency_id')
    tmp3_down_payment_sheet = fields.Monetary(currency_field='currency_id')
    tmp3_advance_payment = fields.Monetary(currency_field='currency_id')
    tmp3_balance_amount = fields.Monetary(currency_field='currency_id')
    tmp3_warranty_month = fields.Integer()
    tmp3_installment_no = fields.Integer()
    tmp3_green_cash_price = fields.Boolean(compute='compute_tmp3_approval_colors', store=True)
    tmp3_green_price = fields.Boolean(compute='compute_tmp3_approval_colors', store=True)
    tmp3_green_downpaymet = fields.Boolean(compute='compute_tmp3_approval_colors', store=True)
    tmp3_green_installment = fields.Boolean(compute='compute_tmp3_approval_colors', store=True)
    tmp3_green_warranty = fields.Boolean(compute='compute_tmp3_approval_colors', store=True)

    tmp4_name = fields.Char(compute='_compute_checkpoint_data')
    tmp4_cash_price = fields.Float(compute='_compute_checkpoint_data')
    tmp4_policy_price = fields.Float(compute='_compute_checkpoint_data')
    tmp4_down_payment = fields.Float(compute='_compute_checkpoint_data')
    tmp4_no_of_installment = fields.Integer(compute='_compute_checkpoint_data')
    tmp4_warranty = fields.Integer(compute='_compute_checkpoint_data')
    tmp4_ups = fields.Char(compute='_compute_checkpoint_data')
    tmp4_transportation = fields.Char(compute='_compute_checkpoint_data')
    tmp4_any_other = fields.Char(compute='_compute_checkpoint_data')
    tmp4_cash_price_sheet = fields.Monetary(currency_field='currency_id')
    tmp4_amount_total = fields.Monetary(currency_field='currency_id')
    tmp4_down_payment_sheet = fields.Monetary(currency_field='currency_id')
    tmp4_advance_payment = fields.Monetary(currency_field='currency_id')
    tmp4_balance_amount = fields.Monetary(currency_field='currency_id')
    tmp4_warranty_month = fields.Integer()
    tmp4_installment_no = fields.Integer()
    tmp4_green_cash_price = fields.Boolean(compute='compute_tmp4_approval_colors', store=True)
    tmp4_green_price = fields.Boolean(compute='compute_tmp4_approval_colors', store=True)
    tmp4_green_downpaymet = fields.Boolean(compute='compute_tmp4_approval_colors', store=True)
    tmp4_green_installment = fields.Boolean(compute='compute_tmp4_approval_colors', store=True)
    tmp4_green_warranty = fields.Boolean(compute='compute_tmp4_approval_colors', store=True)

    tmp5_name = fields.Char(compute='_compute_checkpoint_data')
    tmp5_cash_price = fields.Float(compute='_compute_checkpoint_data')
    tmp5_policy_price = fields.Float(compute='_compute_checkpoint_data')
    tmp5_down_payment = fields.Float(compute='_compute_checkpoint_data')
    tmp5_no_of_installment = fields.Integer(compute='_compute_checkpoint_data')
    tmp5_warranty = fields.Integer(compute='_compute_checkpoint_data')
    tmp5_ups = fields.Char(compute='_compute_checkpoint_data')
    tmp5_transportation = fields.Char(compute='_compute_checkpoint_data')
    tmp5_any_other = fields.Char(compute='_compute_checkpoint_data')
    tmp5_cash_price_sheet = fields.Monetary(currency_field='currency_id')
    tmp5_amount_total = fields.Monetary(currency_field='currency_id')
    tmp5_down_payment_sheet = fields.Monetary(currency_field='currency_id')
    tmp5_advance_payment = fields.Monetary(currency_field='currency_id')
    tmp5_balance_amount = fields.Monetary(currency_field='currency_id')
    tmp5_warranty_month = fields.Integer()
    tmp5_installment_no = fields.Integer()
    tmp5_green_cash_price = fields.Boolean(compute='compute_tmp5_approval_colors', store=True)
    tmp5_green_price = fields.Boolean(compute='compute_tmp5_approval_colors', store=True)
    tmp5_green_downpaymet = fields.Boolean(compute='compute_tmp5_approval_colors', store=True)
    tmp5_green_installment = fields.Boolean(compute='compute_tmp5_approval_colors', store=True)
    tmp5_green_warranty = fields.Boolean(compute='compute_tmp5_approval_colors', store=True)

    is_readonly_sheet_values = fields.Boolean(compute='compute_is_readonly_sheet_values')

    # dup_down_payment_amount = fields.Monetary(currency_field='currency_id', related='down_payment_amount')
    # dup_month_of_warranty = fields.Integer(related='month_of_warranty')
    total_no_installment = fields.Integer(compute='compute_total_no_installment', store=True)

    price_comment1 = fields.Char()
    price_comment2 = fields.Char()
    price_comment3 = fields.Char()
    price_comment4 = fields.Char()
    price_comment5 = fields.Char()
    down_payment_comment1 = fields.Char()
    down_payment_comment2 = fields.Char()
    down_payment_comment3 = fields.Char()
    down_payment_comment4 = fields.Char()
    down_payment_comment5 = fields.Char()
    installment_comment1 = fields.Char()
    installment_comment2 = fields.Char()
    installment_comment3 = fields.Char()
    installment_comment4 = fields.Char()
    installment_comment5 = fields.Char()
    warranty_comment1 = fields.Char()
    warranty_comment2 = fields.Char()
    warranty_comment3 = fields.Char()
    warranty_comment4 = fields.Char()
    warranty_comment5 = fields.Char()
    ups_comment1 = fields.Char()
    ups_comment2 = fields.Char()
    ups_comment3 = fields.Char()
    ups_comment4 = fields.Char()
    ups_comment5 = fields.Char()
    transportation_comment1 = fields.Char()
    transportation_comment2 = fields.Char()
    transportation_comment3 = fields.Char()
    transportation_comment4 = fields.Char()
    transportation_comment5 = fields.Char()
    other_comment1 = fields.Char()
    other_comment2 = fields.Char()
    other_comment3 = fields.Char()
    other_comment4 = fields.Char()
    other_comment5 = fields.Char()

    show_block1 = fields.Boolean(compute='_compute_checkpoint_data')
    show_block2 = fields.Boolean(compute='_compute_checkpoint_data')
    show_block3 = fields.Boolean(compute='_compute_checkpoint_data')
    show_block4 = fields.Boolean(compute='_compute_checkpoint_data')
    show_block5 = fields.Boolean(compute='_compute_checkpoint_data')

    all_template_name = fields.Char(compute='compute_all_template_values')
    total_approval_sheet_price = fields.Monetary(currency_field='currency_id', compute='compute_all_template_values')
    total_approval_sheet_downpayment = fields.Monetary(currency_field='currency_id',
                                                       compute='compute_all_template_values')

    visible_to_user = fields.Boolean(compute='compute_visible_to_user', search='search_visible_to_user', store=False)
    payment_term_type = fields.Selection([
        ('full', 'Full Payment'),
        ('installment', 'Installment'),
        ('cash_credit', 'Cash With Credit'),
    ], related='payment_term_id.term_type')

    @api.depends('quotation_template_ids', 'tmp1_amount_total', 'tmp2_amount_total', 'tmp3_amount_total',
                 'tmp4_amount_total', 'tmp5_amount_total', 'tmp1_down_payment_sheet', 'tmp2_down_payment_sheet',
                 'tmp3_down_payment_sheet', 'tmp4_down_payment_sheet', 'tmp5_down_payment_sheet')
    def compute_all_template_values(self):
        for rec in self:
            name_str = ' & '.join(rec.quotation_template_ids.mapped('name'))
            total_price = rec.tmp1_amount_total + rec.tmp2_amount_total + rec.tmp3_amount_total + rec.tmp4_amount_total + rec.tmp5_amount_total
            total_downpayment = rec.tmp1_down_payment_sheet + rec.tmp2_down_payment_sheet + rec.tmp3_down_payment_sheet + rec.tmp4_down_payment_sheet + rec.tmp5_down_payment_sheet
            rec.total_approval_sheet_price = total_price
            rec.total_approval_sheet_downpayment = total_downpayment
            rec.all_template_name = name_str

    @api.depends('quotation_template_ids')
    def compute_is_readonly_sheet_values(self):
        for rec in self:
            rec.is_readonly_sheet_values = True if len(rec.quotation_template_ids) <= 1 else False

    @api.depends('cash_price_amount', 'so_advance_amount')
    def compute_so_balance_amount(self):
        for rec in self:
            rec.so_balance_amount = rec.cash_price_amount - rec.so_advance_amount

    @api.depends('tmp1_amount_total', 'tmp1_policy_price', 'tmp1_down_payment_sheet', 'tmp1_down_payment',
                 'tmp1_warranty', 'tmp1_warranty_month', 'tmp1_no_of_installment', 'tmp1_installment_no')
    def compute_tmp1_approval_colors(self):
        for rec in self:
            rec.tmp1_green_cash_price = True if rec.tmp1_cash_price_sheet >= rec.tmp1_cash_price else False
            rec.tmp1_green_price = True if rec.tmp1_amount_total >= rec.tmp1_policy_price else False
            rec.tmp1_green_downpaymet = True if rec.tmp1_down_payment_sheet >= rec.tmp1_down_payment else False
            rec.tmp1_green_warranty = True if rec.tmp1_warranty >= rec.tmp1_warranty_month else False
            rec.tmp1_green_installment = True if rec.tmp1_no_of_installment >= rec.tmp1_installment_no else False

    @api.depends('tmp2_amount_total', 'tmp2_policy_price', 'tmp2_down_payment_sheet', 'tmp2_down_payment',
                 'tmp2_warranty', 'tmp2_warranty_month', 'tmp2_no_of_installment', 'tmp2_installment_no')
    def compute_tmp2_approval_colors(self):
        for rec in self:
            rec.tmp2_green_cash_price = True if rec.tmp2_cash_price_sheet >= rec.tmp2_cash_price else False
            rec.tmp2_green_price = True if rec.tmp2_amount_total >= rec.tmp2_policy_price else False
            rec.tmp2_green_downpaymet = True if rec.tmp2_down_payment_sheet >= rec.tmp2_down_payment else False
            rec.tmp2_green_warranty = True if rec.tmp2_warranty >= rec.tmp2_warranty_month else False
            rec.tmp2_green_installment = True if rec.tmp2_no_of_installment >= rec.tmp2_installment_no else False

    @api.depends('tmp3_amount_total', 'tmp3_policy_price', 'tmp3_down_payment_sheet', 'tmp3_down_payment',
                 'tmp3_warranty', 'tmp3_warranty_month', 'tmp3_no_of_installment', 'tmp3_installment_no')
    def compute_tmp3_approval_colors(self):
        for rec in self:
            rec.tmp3_green_cash_price = True if rec.tmp3_cash_price_sheet >= rec.tmp3_cash_price else False
            rec.tmp3_green_price = True if rec.tmp3_amount_total >= rec.tmp3_policy_price else False
            rec.tmp3_green_downpaymet = True if rec.tmp3_down_payment_sheet >= rec.tmp3_down_payment else False
            rec.tmp3_green_warranty = True if rec.tmp3_warranty >= rec.tmp3_warranty_month else False
            rec.tmp3_green_installment = True if rec.tmp3_no_of_installment >= rec.tmp3_installment_no else False

    @api.depends('tmp4_amount_total', 'tmp4_policy_price', 'tmp4_down_payment_sheet', 'tmp4_down_payment',
                 'tmp4_warranty', 'tmp4_warranty_month', 'tmp4_no_of_installment', 'tmp4_installment_no')
    def compute_tmp4_approval_colors(self):
        for rec in self:
            rec.tmp4_green_cash_price = True if rec.tmp4_cash_price_sheet >= rec.tmp4_cash_price else False
            rec.tmp4_green_price = True if rec.tmp4_amount_total >= rec.tmp4_policy_price else False
            rec.tmp4_green_downpaymet = True if rec.tmp4_down_payment_sheet >= rec.tmp4_down_payment else False
            rec.tmp4_green_warranty = True if rec.tmp4_warranty >= rec.tmp4_warranty_month else False
            rec.tmp4_green_installment = True if rec.tmp4_no_of_installment >= rec.tmp4_installment_no else False

    @api.depends('tmp5_amount_total', 'tmp5_policy_price', 'tmp5_down_payment_sheet', 'tmp5_down_payment',
                 'tmp5_warranty', 'tmp5_warranty_month', 'tmp5_no_of_installment', 'tmp5_installment_no')
    def compute_tmp5_approval_colors(self):
        for rec in self:
            rec.tmp5_green_cash_price = True if rec.tmp5_cash_price_sheet >= rec.tmp5_cash_price else False
            rec.tmp5_green_price = True if rec.tmp5_amount_total >= rec.tmp5_policy_price else False
            rec.tmp5_green_downpaymet = True if rec.tmp5_down_payment_sheet >= rec.tmp5_down_payment else False
            rec.tmp5_green_warranty = True if rec.tmp5_warranty >= rec.tmp5_warranty_month else False
            rec.tmp5_green_installment = True if rec.tmp5_no_of_installment >= rec.tmp5_installment_no else False

    @api.onchange('quotation_template_ids', 'total_exp_amount', 'amount_total', 'down_payment_amount',
                  'total_no_installment', 'month_of_warranty', 'cash_price_amount')
    def onchange_approval_sheet_values(self):
        if len(self.quotation_template_ids) <= 1:
            self.tmp1_cash_price_sheet = self.amount_total - self.total_exp_amount
            self.tmp1_amount_total = self.amount_total - self.total_exp_amount
            self.tmp1_down_payment_sheet = self.down_payment_amount
            self.tmp1_warranty_month = self.month_of_warranty
            self.tmp1_installment_no = self.total_no_installment
            self.tmp1_advance_payment = self.so_advance_amount
            self.tmp1_balance_amount = self.so_balance_amount
        else:
            pass

    @api.depends('quotation_template_ids', 'payment_term_id', 'cash_price_amount')
    def _compute_checkpoint_data(self):
        for order in self:
            for i in range(5):
                attr_tmp_name = "tmp{}_name".format(i + 1)
                attr_cash_price = "tmp{}_cash_price".format(i + 1)
                attr_policy_price = "tmp{}_policy_price".format(i + 1)
                attr_down_payment = "tmp{}_down_payment".format(i + 1)
                attr_no_of_installment = "tmp{}_no_of_installment".format(i + 1)
                attr_warranty = "tmp{}_warranty".format(i + 1)
                attr_ups = "tmp{}_ups".format(i + 1)
                attr_transportation = "tmp{}_transportation".format(i + 1)
                attr_any_other = "tmp{}_any_other".format(i + 1)
                attr_show_block = "show_block{}".format(i + 1)

                if order.payment_term_type == 'installment':
                    attr_tmp_name_val = order.quotation_template_ids[i].name if i < len(
                        order.quotation_template_ids) else ''
                    attr_cash_price_val = 0
                    attr_policy_price_val = order.quotation_template_ids[i].policy_price if i < len(
                        order.quotation_template_ids) else ''
                    attr_down_payment_val = order.quotation_template_ids[i].down_payment if i < len(
                        order.quotation_template_ids) else ''
                    attr_no_of_installment_val = order.quotation_template_ids[i].no_of_installment if i < len(
                        order.quotation_template_ids) else ''
                    attr_warranty_val = order.quotation_template_ids[i].warranty if i < len(
                        order.quotation_template_ids) else ''
                    attr_ups_val = order.quotation_template_ids[i].ups if i < len(order.quotation_template_ids) else ''
                    attr_transportation_val = order.quotation_template_ids[i].transportation if i < len(
                        order.quotation_template_ids) else ''
                    attr_any_other_val = ''
                    attr_show_block_val = True if i < len(order.quotation_template_ids) else False
                else:
                    attr_tmp_name_val = order.quotation_template_ids[i].name if i < len(
                        order.quotation_template_ids) else ''
                    attr_cash_price_val = order.quotation_template_ids[i].credit_cash_price if i < len(
                        order.quotation_template_ids) else ''
                    attr_policy_price_val = 0
                    attr_down_payment_val = order.quotation_template_ids[i].credit_down_payment if i < len(
                        order.quotation_template_ids) else ''
                    attr_no_of_installment_val = order.quotation_template_ids[i].credit_no_of_installment if i < len(
                        order.quotation_template_ids) else ''
                    attr_warranty_val = order.quotation_template_ids[i].credit_warranty if i < len(
                        order.quotation_template_ids) else ''
                    attr_ups_val = order.quotation_template_ids[i].credit_ups if i < len(order.quotation_template_ids) else ''
                    attr_transportation_val = order.quotation_template_ids[i].credit_transportation if i < len(
                        order.quotation_template_ids) else ''
                    attr_any_other_val = ''
                    attr_show_block_val = True if i < len(order.quotation_template_ids) else False
                setattr(order, attr_tmp_name, attr_tmp_name_val)
                setattr(order, attr_cash_price, attr_cash_price_val)
                setattr(order, attr_policy_price, attr_policy_price_val)
                setattr(order, attr_down_payment, attr_down_payment_val)
                setattr(order, attr_no_of_installment, attr_no_of_installment_val)
                setattr(order, attr_warranty, attr_warranty_val)
                setattr(order, attr_ups, attr_ups_val)
                setattr(order, attr_transportation, attr_transportation_val)
                setattr(order, attr_any_other, attr_any_other_val)
                setattr(order, attr_show_block, attr_show_block_val)

    @api.onchange('quotation_template_ids')
    def onchange_quotation_template_ids(self):
        if not self.quotation_template_ids:
            return
        # if not self.quotation_template_ids:
        #     self.require_signature = self._get_default_require_signature()
        #     self.require_payment = self._get_default_require_payment()
        #     return
        templates = self.quotation_template_ids.with_context(lang=self.partner_id.lang)

        order_lines_data = [fields.Command.clear()]
        option_lines_data = [fields.Command.clear()]
        for template in templates:
            order_lines_data += [
                fields.Command.create(line._prepare_order_line_values())
                for line in template.sale_order_template_line_ids
            ]
            option_lines_data += [
                fields.Command.create(option._prepare_option_line_values())
                for option in template.sale_order_template_option_ids
            ]
        if len(order_lines_data) >= 2:
            order_lines_data[1][2]['sequence'] = -99

        self.order_line = order_lines_data
        self.sale_order_option_ids = option_lines_data

        if templates and templates[0].number_of_days > 0:
            self.validity_date = fields.Date.context_today(self) + timedelta(templates[0].number_of_days)

        if templates and templates[0].note:
            self.note = templates[0].note

    @api.depends('state', 'hierarchy_approval_seq', 'approval_ids', 'hierarchy_last_approver_id')
    def compute_visible_to_user(self):
        hierarchy_id = self.env['sale.approval.hierarchy'].search([], limit=1)
        loggedin_user = self.env.user if self.env.user.id != 1 else self.env['res.users'].browse(
            self.env.context.get('uid', False))
        for rec in self:
            if loggedin_user.has_group('sales_team.group_sale_manager'):
                rec.visible_to_user = True
            elif loggedin_user.has_group('sales_team.group_sale_salesman_all_leads') or self.env.user.has_group(
                    'sales_team.group_sale_salesman'):
                visible_to_user = False
                if loggedin_user.id in rec.approval_ids.ids:
                    visible_to_user = True
                elif hierarchy_id:
                    restricted_users = hierarchy_id.sale_hierarchy_lines.filtered(
                        lambda item: item.restrict_visibility).user_ids.ids
                    if loggedin_user.id not in restricted_users:
                        visible_to_user = True
                rec.visible_to_user = visible_to_user
            else:
                rec.visible_to_user = False

    # @api.model
    def search_visible_to_user(self, operator, value):
        if (operator == '=' and value) or (operator == '!=' and not value):
            sale_orders = self.search([]).filtered(lambda item: item.visible_to_user)
        else:
            sale_orders = self.search([]).filtered(lambda item: not item.visible_to_user)
        return [('id', 'in', sale_orders.ids)]

    @api.depends('phase1_each_installment', 'phase2_each_installment', 'last_installment_amount',
                 'phase1_installment_no', 'phase2_installment_no')
    def compute_total_no_installment(self):
        for rec in self:
            total = 0
            if rec.phase1_each_installment:
                total += rec.phase1_installment_no
            if rec.phase2_each_installment:
                total += rec.phase2_installment_no - rec.phase1_installment_no
            if rec.last_installment_amount:
                total += 1
            rec.total_no_installment = total

    @api.onchange('phase1_each_installment', 'phase2_each_installment', 'last_installment_amount',
                  'phase1_installment_no', 'phase2_installment_no')
    def onchange_total_no_installment_depends(self):
        for rec in self:
            if len(rec.quotation_template_ids) <= 1:
                total = 0
                if rec.phase1_each_installment:
                    total += rec.phase1_installment_no
                if rec.phase2_each_installment:
                    total += rec.phase2_installment_no - rec.phase1_installment_no
                if rec.last_installment_amount:
                    total += 1
                rec.tmp1_installment_no = total

    @api.depends('bp_amount', 'other_exp1_amount', 'other_exp2_amount')
    def compute_total_expt_amount(self):
        for rec in self:
            rec.total_exp_amount = rec.bp_amount + rec.other_exp1_amount + rec.other_exp2_amount

    @api.depends('amount_total', 'down_payment_amount')
    def compute_res_amount(self):
        for rec in self:
            rec.remaining_amount = rec.amount_total - rec.down_payment_amount

    @api.depends('remaining_amount', 'phase1_installment_no', 'phase1_each_installment')
    def compute_readonly_phase2(self):
        for rec in self:
            paid_installment_amount = rec.phase1_installment_no * rec.phase1_each_installment
            rec.is_readonly_phase2 = True if paid_installment_amount >= rec.remaining_amount else False
            rec.phase2_init_installment_no = rec.phase1_installment_no + 1
            if rec.is_readonly_phase2:
                rec.phase2_each_installment = 0
                # rec.last_installment_amount = 0

    @api.depends('remaining_amount', 'phase1_installment_no', 'phase1_each_installment', 'phase2_init_installment_no',
                 'phase2_installment_no', 'phase2_each_installment')
    def compute_last_installments(self):
        for rec in self:
            paid_installment_amount = 0
            paid_installment_amount += (rec.phase1_installment_no * rec.phase1_each_installment)
            paid_installment_amount += (
                    (rec.phase2_installment_no - rec.phase1_installment_no) * rec.phase2_each_installment)
            rec.last_installment_amount = rec.remaining_amount - paid_installment_amount

    @api.onchange('phase1_installment_no')
    def _onchange_phase2_installment_no(self):
        self.phase2_installment_no = max(self.phase2_installment_no, self.phase1_installment_no + 1)

    @api.model
    def create(self, values):
        if values.get('partner_id', False) != values.get('partner_shipping_id', False):
            values['partner_shipping_id'] = values.get('partner_id', False)

        res = super(SaleOrderInherit, self).create(values)

        phase1_installment_no = res.phase1_installment_no
        phase1_each_installment = res.phase1_each_installment
        phase2_installment_no = res.phase2_installment_no
        phase2_each_installment = res.phase2_each_installment
        remaining_amount = res.remaining_amount

        paid_installment_amount = 0
        paid_installment_amount += (phase1_installment_no * phase1_each_installment)
        paid_installment_amount += ((phase2_installment_no - phase1_installment_no) * phase2_each_installment)
        if paid_installment_amount > remaining_amount:
            raise ValidationError('Installment Configuration Is Not Correct.')

        hierarchy_id = self.env.ref('custom_sale_order.sale_approval_hierarchy_record')
        hierarchy_sequences = hierarchy_id and hierarchy_id.sale_hierarchy_lines and hierarchy_id.sale_hierarchy_lines[
            0]
        consumable = True if any(
            line.product_id and line.product_id.type != 'product' for line in self.order_line) else False
        if hierarchy_sequences and hierarchy_sequences.user_ids and consumable == False:
            res.approval_ids = [(6, 0, hierarchy_sequences.user_ids.ids)]
            res.hierarchy_approval_seq = 0
            if res.approval_ids:
                self.env.ref('custom_sale_order.sale_approval_request_mail').send_mail(res.id, force_send=True)
        return res

    def write(self, values):
        res = super(SaleOrderInherit, self).write(values)
        phase1_installment_no = self.phase1_installment_no
        phase1_each_installment = self.phase1_each_installment
        phase2_installment_no = self.phase2_installment_no
        phase2_each_installment = self.phase2_each_installment
        remaining_amount = self.remaining_amount

        paid_installment_amount = 0
        paid_installment_amount += (phase1_installment_no * phase1_each_installment)
        paid_installment_amount += ((phase2_installment_no - phase1_installment_no) * phase2_each_installment)
        if paid_installment_amount > remaining_amount:
            raise ValidationError('Installment Configuration Is Not Correct.')
        return

    def hierarchy_approval(self):
        self.ensure_one()
        # self._check_security_action_approve()
        hierarchy_id = self.env.ref('custom_sale_order.sale_approval_hierarchy_record')
        if hierarchy_id:
            hierarchy_sequences = hierarchy_id.sale_hierarchy_lines[
                self.hierarchy_approval_seq + 1] if self.hierarchy_approval_seq + 1 < len(
                hierarchy_id.sale_hierarchy_lines) else False
            if hierarchy_sequences and hierarchy_sequences.user_ids:
                self.hierarchy_last_approver_id = self.env.user.id
                self.approval_ids = [(6, 0, hierarchy_sequences.user_ids.ids)]
                self.hierarchy_approval_seq = self.hierarchy_approval_seq + 1
                self.message_post(body=_(
                    "<p><strong><span class='fa fa-sun-o'></span></strong> <span>Sale Order Approval</span> done by <span> " + str(
                        self.env.user.name) + "</span></p>"))
                if self.approval_ids:
                    self.env.ref('custom_sale_order.sale_approval_request_mail').send_mail(self.id, force_send=True)
                return True

        self.hierarchy_last_approver_id = self.env.user.id
        self.message_post(body=_(
            "<p><strong><span class='fa fa-sun-o'></span></strong> <span>Sale Order Approval</span> done by <span> " + str(
                self.env.user.name) + "</span></p>"))
        self.approval_ids = False
        return True


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    quotation_template_id = fields.Many2one('sale.order.template')
    quotation_template_line_id = fields.Many2one('sale.order.template.line')
    is_master_product = fields.Boolean(default=False)
