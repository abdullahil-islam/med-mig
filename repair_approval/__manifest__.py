# -*- coding: utf-8 -*-
{
    'name': "MISL Repair Approval",

    'summary': """
        MISL Repair Approval""",

    'description': """
        MISL Repair Approval
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
    'depends': ['repair_maintenance'],

    # always loaded
    'data': [
        "security/ir.model.access.csv",
        "data/invoice_hierarchy.xml",
        "data/data.xml",
        "views/repair_approval_config_view.xml",

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}