# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InheritResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_name(self):
        partner = self
        name = super(InheritResPartner, self)._get_name()

        if self.phone:
            name = name + "\n" + partner.phone
        if self.mobile:
            name = name + "\n" + partner.mobile
        return name.strip()
