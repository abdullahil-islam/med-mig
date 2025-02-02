# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model
    def create(self, vals):
        result = super(IrAttachment, self).create(vals)
        file_size = (result.file_size/3000)
        if result.file_size and result.res_model in ('maintenance.request', 'repair.order', 'project.project', 'project.task') and file_size >= 3000:
            raise ValidationError("File size must be less than 3 MB.")
        return result

    
    def write(self, vals):
        result = super(IrAttachment, self).write(vals)
        for rec in self:
            file_size = (rec.file_size/3000)
            if rec.file_size and rec.res_model in ('maintenance.request', 'repair.order' 'project.project', 'project.task') and file_size >= 3000:
                raise ValidationError("File size must be less than 3 MB.")
        return result
