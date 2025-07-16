# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID
from . import models
from . import wizard


def post_init_hook(cr, registry):
    """
    Generate API key to use for API requests from designer to Odoo.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    teams = env['crm.team'].search([])
    for team in teams:
        team._update_zone_mappings()
    leads = env['crm.lead'].search([])
    leads.compute_allowed_address_fields()
