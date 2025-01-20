# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    
    def _get_user_details(self):
        context = self._context
        login_user = self.env['res.users'].sudo().browse(context.get('uid'))
        admin_uid = self.env.ref('base.user_admin').id
        res = False
        if login_user.id in (SUPERUSER_ID, admin_uid):
            res = True
        self.is_admin_user_temp = res
        self.is_admin_user = self.is_admin_user_temp

    is_admin_user_temp = fields.Boolean(string='Is Admin Temp', compute='_get_user_details')
    is_admin_user = fields.Boolean(string='Is Admin')
    
    
class MailActivity(models.Model):
    _inherit = 'mail.activity'
    _description = 'Activity'

    @api.model
    def create(self, vals):
        if self._context.get('default_res_model') == 'maintenance.request':
            self = self.sudo() 
        return super(MailActivity, self).create(vals)

    @api.model
    def get_domain(self):
        if self._context.get('default_res_model') and self._context.get('default_res_id') and self._context.get('default_res_model') == 'maintenance.request':
            follower_ids = self.env[self._context['default_res_model']].browse(self._context['default_res_id']).mapped('user_ids')
            return [('id', 'in', follower_ids.ids)]
        return [('id', 'in', self.env['res.users'].search([]).ids)]

    @api.model
    def set_user(self):
        if self._context.get('default_res_model') and self._context.get('default_res_id') and self._context.get('default_res_model') == 'maintenance.request':
            follower_ids = self.env[self._context['default_res_model']].browse(self._context['default_res_id']).mapped('user_ids')
            return follower_ids.ids and follower_ids.ids[0] or False
        return self.env.user.id

    user_id = fields.Many2one(
        'res.users', 'Assigned to',
        default=set_user,
        index=True, required=True, domain=get_domain)
