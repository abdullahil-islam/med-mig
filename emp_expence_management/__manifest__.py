# -*- coding: utf-8 -*-
{
    'name': "emp_expence_management",

    'summary': """
        Expence management""",

    'description': """
        Expence management
    """,

    'author': 'Medionics',
    'website': 'https://medionicsbd.com/',
    'maintainer': 'Shams',
    'support': 'shams@medionicsbd.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'expenses',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_expense'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/ex_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
