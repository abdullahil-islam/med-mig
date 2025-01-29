# -*- encoding: utf-8 -*-
{
    'name': 'Odoo Web Login Screen',
    'summary': 'The new configurable Odoo Web Login Screen',
    'version': '12.0.1.0',
    'category': 'Website',
    'summary': """
The new configurable Odoo Web Login Screen
""",
    'author': 'Medionics',
    'website': 'https://medionicsbd.com/',
    'maintainer': 'Shams',
    'support': 'shams@medionicsbd.com',
    'license': 'AGPL-3',
    'depends': [
    ],
    'data': [
        'data/ir_config_parameter.xml',
        'templates/website_templates.xml',
        'templates/webclient_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'odoo_web_login/static/src/css/web_login_style.css'
        ]
    },
    'installable': True,
    'application': True,
}
