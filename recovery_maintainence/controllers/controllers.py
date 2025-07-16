# -*- coding: utf-8 -*-
from odoo import http

# class RecoveryMaintainence(http.Controller):
#     @http.route('/recovery_maintainence/recovery_maintainence/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/recovery_maintainence/recovery_maintainence/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('recovery_maintainence.listing', {
#             'root': '/recovery_maintainence/recovery_maintainence',
#             'objects': http.request.env['recovery_maintainence.recovery_maintainence'].search([]),
#         })

#     @http.route('/recovery_maintainence/recovery_maintainence/objects/<model("recovery_maintainence.recovery_maintainence"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('recovery_maintainence.object', {
#             'object': obj
#         })