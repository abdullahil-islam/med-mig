# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _

class CRM(models.Model):
    _inherit = 'crm.lead'

    def attachment_tree_view(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['domain'] = str([
            ('res_model', '=', 'crm.lead'),
            ('res_id', 'in', self.ids),
        ])
        action['context'] = "{'default_res_model': '%s','default_res_id': %d}" % ('crm.lead', self.id)
        return action
    
    def _compute_attached_docs_count(self):
        Attachment = self.env['ir.attachment']
        for project in self:
            project.doc_count = Attachment.search_count([
                ('res_model', '=', 'crm.lead'), ('res_id', '=', project.id),
            ])
    
    doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Number of documents attached")
    planned_revenue = fields.Monetary('Expected Price', currency_field='company_currency', track_visibility='always')
    sub_city_id = fields.Many2one('res.sub.city')
    city_id = fields.Many2one('res.city')

    @api.onchange('sub_city_id')
    def onchange_sub_city_id(self):
        if self.sub_city_id:
            self.city = self.sub_city_id.city_id.name
            self.city_id = self.sub_city_id.city_id.id
            self.state_id = self.sub_city_id.state_id.id if self.sub_city_id.state_id else False
            self.country_id = self.sub_city_id.country_id.id

    @api.onchange('city_id')
    def onchange_city_id(self):
        if self.city_id:
            self.city = self.city_id.name
            self.state_id = self.city_id.state_id.id if self.city_id.state_id else False
            self.country_id = self.city_id.country_id.id

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        """ Extract data from lead to create a partner.

        :param name : furtur name of the partner
        :param is_company : True if the partner is a company
        :param parent_id : id of the parent partner (False if no parent)

        :return: dictionary of values to give at res_partner.create()
        """
        res = super(CRM, self)._prepare_customer_values(partner_name=partner_name, is_company=is_company, parent_id=parent_id)
        res.update({
            'sub_city_id': self.sub_city_id.id,
            'city_id': self.city_id.id,
        })
        return res

