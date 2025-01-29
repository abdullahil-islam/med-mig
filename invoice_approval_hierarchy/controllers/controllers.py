# -*- coding: utf-8 -*-
from odoo import http

# class InvoiceApprovalHierarchy(http.Controller):
#     @http.route('/invoice_approval_hierarchy/invoice_approval_hierarchy/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_approval_hierarchy/invoice_approval_hierarchy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_approval_hierarchy.listing', {
#             'root': '/invoice_approval_hierarchy/invoice_approval_hierarchy',
#             'objects': http.request.env['invoice_approval_hierarchy.invoice_approval_hierarchy'].search([]),
#         })

#     @http.route('/invoice_approval_hierarchy/invoice_approval_hierarchy/objects/<model("invoice_approval_hierarchy.invoice_approval_hierarchy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_approval_hierarchy.object', {
#             'object': obj
#         })