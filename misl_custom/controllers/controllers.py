# -*- coding: utf-8 -*-
from odoo import http

# class /opt/projects/samsProject/mislCustom(http.Controller):
#     @http.route('//opt/projects/sams_project/misl_custom//opt/projects/sams_project/misl_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//opt/projects/sams_project/misl_custom//opt/projects/sams_project/misl_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/opt/projects/sams_project/misl_custom.listing', {
#             'root': '//opt/projects/sams_project/misl_custom//opt/projects/sams_project/misl_custom',
#             'objects': http.request.env['/opt/projects/sams_project/misl_custom./opt/projects/sams_project/misl_custom'].search([]),
#         })

#     @http.route('//opt/projects/sams_project/misl_custom//opt/projects/sams_project/misl_custom/objects/<model("/opt/projects/sams_project/misl_custom./opt/projects/sams_project/misl_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/opt/projects/sams_project/misl_custom.object', {
#             'object': obj
#         })