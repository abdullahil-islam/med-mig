# -*- coding: utf-8 -*-

{
    'name': 'Transport Document Notification',
    'version': '1.0.1',
    'sequence': 2,
    'category': 'Purchase',
    'summary': 'Notify expire documents',
    'description': """
Transport Document Notification
==================================
* Notify before documents expire.
    """,
    'author': 'Medionics',
    'website': 'https://medionicsbd.com/',
    'maintainer': 'Shams',
    'support': 'shams@medionicsbd.com',
    'depends': ['repair_maintenance'],
    'data': [
        # 'views/templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'transport_document_notification/static/src/js/systray_document_notification_menu.js',
            'transport_document_notification/static/src/xml/document_expiry.xml',
        ],
    },
    'installable': True,
    'application': True
}
