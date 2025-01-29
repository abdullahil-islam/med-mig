# -*- coding: utf-8 -*-

{
    'name': 'Employee Leave Multi Approval Hierarchy',
    'category': 'HR',
    'version': '12.0',
    'author': 'Medionics',
    'website': 'https://medionicsbd.com/',
     'maintainer': 'Shams',
     'support': 'shams@medionicsbd.com',

    'summary': """Employee Leave Multi Approval Hierarchy""",
    'description': """
        This plugin use for Employee Leave Multi approval Hierarchy
    """,
    'depends': ['hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/hr_department_view.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
}


