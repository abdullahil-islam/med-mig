# -*- coding: utf-8 -*-
{
    'name': "invoice_approval_hierarchy",

    'summary': """
        Sale Invoice approval Hierarchy""",

    'description': """
        Sale invoice approval hierarchy, Admin can able to set approval hierarchy of multiple users.
    """,

    'author': 'Medionics',
    'website': 'https://medionicsbd.com/',
    'maintainer': 'Shams',
    'support': 'shams@medionicsbd.com',


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'invoice',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/invoice_hierarchy.xml',
        'data/data.xml',
        'views/invoice_views.xml',
    ],
    # only loaded in demonstration mode
}