# -*- coding: utf-8 -*-

from odoo import models, fields, api
from random import randint


class SalesOrderTag(models.Model):
    _name = 'sales.order.tag'
    _description = 'Sales Order Tag'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Tag Name', required=True)
    color = fields.Integer(string='Color', default=_get_default_color)

    _sql_constraints = [
        ('sales_tag_name_uniq', 'unique (name)', "Sales Tag name already exists !"),
    ]
