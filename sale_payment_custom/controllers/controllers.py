# -*- coding: utf-8 -*-
from odoo import http

# class SalePaymentCustom(http.Controller):
#     @http.route('/sale_payment_custom/sale_payment_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_payment_custom/sale_payment_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_payment_custom.listing', {
#             'root': '/sale_payment_custom/sale_payment_custom',
#             'objects': http.request.env['sale_payment_custom.sale_payment_custom'].search([]),
#         })

#     @http.route('/sale_payment_custom/sale_payment_custom/objects/<model("sale_payment_custom.sale_payment_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_payment_custom.object', {
#             'object': obj
#         })