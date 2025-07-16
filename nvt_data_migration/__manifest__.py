{
    'name': 'Database to Odoo Data Migration - N-Hub',
    'version': '1.0.0',
    'category': 'Tools',
    'license': 'OPL-1',
    'price': 49.0,
    'currency': 'USD',
    'summary': 'Tool for migrating data from any PostgreSQL database to Odoo',
    'description': """
Data Migration Tool
===================

This module provides a comprehensive solution to migrate data from any PostgreSQL database into Odoo. 
It allows you to:

- Define data sources with connection parameters.
- Define target models in Odoo with fields mapping.
- Run SQL queries against the source database.
- Automatically map and transform data before importing it into Odoo.
- Handle data transformations such as fixed values, formulas, and various data types.
- Preview data before actual migration.
""",
    'depends': ['base', 'mail'],
    'images': ['static/description/cover_image.png'],
    'support': 'odoo@novitatus.com',
    'demo': [],
    'author': 'Novitatus Hub',
    'website': 'https://www.novitatus.com',
    'data': [
        'views/nvt_data_source_view.xml',
        'views/nvt_data_target_view.xml',
        'views/n_hub_migration_menus.xml',
        'security/ir.model.access.csv',
    ],
    'external_dependencies': {
        'python': ['psycopg2'],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
