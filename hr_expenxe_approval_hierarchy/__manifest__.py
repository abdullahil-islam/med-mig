# -*- coding: utf-8 -*-

{
    'name': 'Employee Expense Multi Approval Hierarchy',
    'category': 'HR-Expense',
    'version': '12.0',
    'author': 'Medionics',
    'website': 'https://medionicsbd.com/',
     'maintainer': 'Shams',
     'support': 'shams@medionicsbd.com',

    'summary': """Employee Expense Multi Approval Hierarchy""",
    'description': """
        This plugin use for Employee Expense Multi approval Hierarchy
    """,
    'depends': ['hr_expense','hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/hr_expense_sheet_view.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
}


