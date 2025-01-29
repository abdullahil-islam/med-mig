# -*- coding: utf-8 -*-
from odoo import http

# class HrCustomization(http.Controller):
#     @http.route('/hr_customization/hr_customization/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_customization/hr_customization/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_customization.listing', {
#             'root': '/hr_customization/hr_customization',
#             'objects': http.request.env['hr_customization.hr_customization'].search([]),
#         })

#     @http.route('/hr_customization/hr_customization/objects/<model("hr_customization.hr_customization"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_customization.object', {
#             'object': obj
#         })