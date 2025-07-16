# -*- coding: utf-8 -*-

from . import controllers
from . import models
from . import report

from odoo import api, SUPERUSER_ID

def sync_compute_visible_to_user(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    sale_order_ids = env['sale.order'].search([])
    sale_order_ids.with_context(make_true=True).compute_visible_to_user()
