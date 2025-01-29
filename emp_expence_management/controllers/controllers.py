# -*- coding: utf-8 -*-
from odoo import http

# class EmpExpenceManagement(http.Controller):
#     @http.route('/emp_expence_management/emp_expence_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/emp_expence_management/emp_expence_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('emp_expence_management.listing', {
#             'root': '/emp_expence_management/emp_expence_management',
#             'objects': http.request.env['emp_expence_management.emp_expence_management'].search([]),
#         })

#     @http.route('/emp_expence_management/emp_expence_management/objects/<model("emp_expence_management.emp_expence_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('emp_expence_management.object', {
#             'object': obj
#         })