# -*- coding: utf-8 -*-
{
    'name': "custom_sale_order",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': 'Medionics',
    'website': 'https://medionicsbd.com/',
    'maintainer': 'Shams',
    'support': 'shams@medionicsbd.com',


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'sale', 'account', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'security/security.xml',
        'data/data.xml',
        'data/sale_approval_hierarchy.xml',
        'views/sale_approval_hierarchy_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/res_config_setting.xml',
        'views/quotation_template_views.xml',
        # 'views/webclient_template.xml',
        'views/payment_term_views.xml',
        'report/medinics_delivery_slip.xml',
        'report/medionics_invoice_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_sale_order/static/src/js/list_renderer.js',
        ]
    },
    # only loaded in demonstration mode
    # 'post_init_hook': 'sync_compute_visible_to_user',
}
