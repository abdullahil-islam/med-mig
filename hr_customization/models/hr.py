# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class Employee(models.Model):
    _inherit = 'hr.employee'

    def attachment_tree_view(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['domain'] = str([
            ('res_model', '=', 'hr.employee'),
            ('res_id', 'in', self.ids),
        ])
        action['context'] = "{'default_res_model': '%s','default_res_id': %d}" % ('hr.employee', self.id)
        return action
    
    def _compute_attached_docs_count(self):
        Attachment = self.env['ir.attachment']
        for project in self:
            project.doc_count = Attachment.search_count([
                ('res_model', '=', 'hr.employee'), ('res_id', '=', project.id),
            ])
    
    doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Number of documents attached")
    att_ids = fields.One2many('ir.attachment', 'res_id',domain=[('res_model', '=', 'hr.employee')], string="Upload your documents")
