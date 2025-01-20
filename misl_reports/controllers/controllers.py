# -*- coding: utf-8 -*-
from odoo import http

# class /opt/mislReports(http.Controller):
#     @http.route('//opt/misl_reports//opt/misl_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//opt/misl_reports//opt/misl_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/opt/misl_reports.listing', {
#             'root': '//opt/misl_reports//opt/misl_reports',
#             'objects': http.request.env['/opt/misl_reports./opt/misl_reports'].search([]),
#         })

#     @http.route('//opt/misl_reports//opt/misl_reports/objects/<model("/opt/misl_reports./opt/misl_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/opt/misl_reports.object', {
#             'object': obj
#         })