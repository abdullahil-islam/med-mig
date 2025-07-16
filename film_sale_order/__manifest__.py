# -*- coding: utf-8 -*-
{
    'name': "Film Sale Order",
    'summary': """""",
    'description': """""",
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'stock', 'sale', 'sale_stock', 'account', 'product'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
        'views/sale_order_views.xml',
        # 'views/register_payment_views.xml',
        'views/account_payment_views.xml',
        'views/product_views.xml',
        'report/inherit_delivery_slip_report.xml',
        'report/money_receipt_report.xml',
        'report/sale_order_bill_report.xml',
        # 'report/medinics_delivery_slip.xml',
    ],
}
