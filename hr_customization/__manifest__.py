# -*- coding: utf-8 -*-
{
    'name': "hr_customization",

    'summary': """
        HR Customization""",

    'description': """
        HR Customization
    """,

    'author': 'Medionics',
    'website': 'https://medionicsbd.com/',
    'maintainer': 'Shams',
    'support': 'shams@medionicsbd.com',


    'category': 'hr',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        'views/hr_views.xml',
    ],
}
