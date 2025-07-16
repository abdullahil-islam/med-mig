# -*- coding: utf-8 -*-
from email.policy import default

from odoo import models, fields, api

class SaleApprovalHierarchy(models.Model):
    _name = 'sale.approval.hierarchy'

    name = fields.Char("Name")
    sale_hierarchy_lines = fields.One2many('sale.approval.hierarchy.line','sale_hierarchy_id',string="Approval Hierarchy")


class SaleApprovalHierarchyLine(models.Model):
    _name = 'sale.approval.hierarchy.line'
    _order = 'sequence asc'

    sequence = fields.Integer("Sequence")
    user_ids = fields.Many2many('res.users')
    sale_hierarchy_id = fields.Many2one('sale.approval.hierarchy', string='Sales Approval')
    restrict_visibility = fields.Boolean(default=False)