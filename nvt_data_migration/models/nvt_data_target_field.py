from odoo import api, fields, models

class NVTDataTargetField(models.Model):
    _name = 'nvt.data.target.field'
    _description = 'Data Target Field'

    target_id = fields.Many2one('nvt.data.target', 'Target', ondelete='cascade')
    
    origin_column = fields.Char(string='Origin Value')

    origin_column_type = fields.Selection([
        ('column', 'Column'),
        ('column_int', 'Column Integer'),
        ('column_float', 'Column Float'),
        ('column_m2m', 'Column M2M'),
        ('fixed', 'Fixed Value'),
        ('fixed_ref', 'Fixed Reference Value'),
        ('formula', 'Formula'),
        ('m2o_external_code', 'Many2One External Code'),
    ], string="Origin Value Type", default='column', help="Type of the origin column's data source.")
    
    field_id = fields.Many2one('ir.model.fields', 'Field', required=True, ondelete='cascade', domain="[('model_id', '=', parent.model_id)]")