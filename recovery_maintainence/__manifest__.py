# -*- coding: utf-8 -*-
{
    'name': "recovery_maintainence",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'maintenance', 'repair_maintenance', 'product'],

    # always loaded
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/sb_type_products.xml',
        'views/product_views.xml',
        'views/account_invoice_view.xml',
        'views/recovery_menus.xml',
        'views/maintenance_status_views.xml',
        'views/account_payment.xml',
        'report/service_bill_report_layout.xml',
        'report/service_bill_report.xml',
        'report/money_receipt_report.xml',
        'views/res_config_setting_views.xml',
    ],
}
