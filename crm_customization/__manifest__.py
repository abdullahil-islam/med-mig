# -*- coding: utf-8 -*-
{
    'name': "crm_customization",

    'summary': """
        crm""",

    'description': """
        Long description of module's purpose
    """,

    'author': 'Medionics',
    'website': 'https://medionicsbd.com/',
    'maintainer': 'Shams',
    'support': 'shams@medionicsbd.com',

    'category': 'crm',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'base_location'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/crm_view.xml',
        'views/res_sub_city_views.xml',
        'views/res_partner_views.xml',
    ],
}
