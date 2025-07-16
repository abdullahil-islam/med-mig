# -*- coding: utf-8 -*-
{
    'name': "Yearly Sale Consumption Report",
    'summary': """""",
    'description': """""",
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
    'depends': ['base', 'sale'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/reports.xml',
        'wizard/yearly_sale_consumption_wizard.xml',
    ],
}
