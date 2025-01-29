# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class InvoiceHierarchy(models.Model):
    _name = 'invoice.hierarchy'
    
    name = fields.Char("Name")
    invoice_hir_ids = fields.One2many('hierarchy.line','invoice_hi_id',string="Approval Hierarchy")
    
    
class InvoiceHierarchyLine(models.Model):
    _name = 'hierarchy.line'
    _order = 'sequence asc'
    
    sequence = fields.Integer("Sequence")
    user_ids = fields.Many2many('res.users')
    invoice_hi_id = fields.Many2one('invoice.hierarchy',string='Invoice Approval')

    
class AccountMove(models.Model):
    _inherit = 'account.move'

    def _display_approve_button(self):
        for rec in self:
            if rec.approval_ids:
                rec.display_validate_button = False
            else:
                rec.display_validate_button = True
            invoice_last_approver = ''
            if rec.invoice_last_approver_id:
                invoice_last_approver += "Last Approved by : " + str(rec.invoice_last_approver_id.name)
                if rec.approval_ids:
                    rec.display_validate_button = False
                    invoice_last_approver += " <br/>Waiting approval from: "
                    for one_approval in rec.approval_ids:
                        invoice_last_approver += str(one_approval.name)+", "
                else:
                    rec.display_validate_button = True
            rec.invoice_last_approver = invoice_last_approver
            rec.approval_pending = False
            if rec.state == 'draft' and self.env.user.id in rec.sudo().approval_ids.ids:
                rec.approval_pending = True
    
    approval_ids = fields.Many2many('res.users')
    invoice_last_approver_id = fields.Many2one('res.users')
    approval_seq = fields.Integer("Approval Sequence")
    approval_pending = fields.Boolean('Approval Pending',compute='_display_approve_button')
    invoice_last_approver = fields.Html(string='Last Approval String', compute='_display_approve_button')
    display_validate_button = fields.Boolean('Display Validate Button',compute='_display_approve_button')

    def invoice_approval(self):
        self.ensure_one()
        # self._check_security_action_approve()
        invoice_app_id = self.env.ref('invoice_approval_hierarchy.invoice_approval_record')
        if invoice_app_id:
            invoice_hierarchy_sequences = invoice_app_id and invoice_app_id.invoice_hir_ids and invoice_app_id.invoice_hir_ids[self.approval_seq+1] if self.approval_seq+1 < len(invoice_app_id.invoice_hir_ids) else False
            if invoice_hierarchy_sequences and invoice_hierarchy_sequences.user_ids:
                self.invoice_last_approver_id = self.env.user.id
                self.approval_ids = [(6, 0, invoice_hierarchy_sequences.user_ids.ids)]
                self.approval_seq = self.approval_seq+1
                self.message_post(body=_("<p><strong><span class='fa fa-sun-o'></span></strong> <span>Invoice Approval</span> done by <span> " + str(self.env.user.name) + "</span></p>"))
                if self.approval_ids:
                    self.env.ref('invoice_approval_hierarchy.invoice_request_mail').send_mail(self.id, force_send=True)
                return True

        self.invoice_last_approver_id = self.env.user.id
        self.message_post(body=_("<p><strong><span class='fa fa-sun-o'></span></strong> <span>Invoice Approval</span> done by <span> " + str(self.env.user.name) + "</span></p>"))
        self.approval_ids = False
        return True
    
    @api.model
    def create(self, values):
        res = super(AccountMove, self).create(values)
        invoice_app_id = self.env.ref('invoice_approval_hierarchy.invoice_approval_record')
        invoice_hierarchy_sequences = invoice_app_id and invoice_app_id.invoice_hir_ids and invoice_app_id.invoice_hir_ids[0]
        consu = False
        sale_order = self.env['sale.order'].search([('name','=', res.invoice_origin)], limit=1)
        if sale_order:
            for rec in sale_order.order_line:
                if rec.product_id and rec.product_id.type != 'product' and rec.product_uom_qty > 0:
                    consu = True
        if invoice_hierarchy_sequences and invoice_hierarchy_sequences.user_ids and res.move_type == 'out_invoice' and consu == False:
            res.approval_ids = [(6,0,invoice_hierarchy_sequences.user_ids.ids)]
            res.approval_seq = 0
            if res.approval_ids:
                self.env.ref('invoice_approval_hierarchy.invoice_request_mail').send_mail(res.id, force_send=True)
        return res

