# -*- coding: utf-8 -*-
{
    'name': "Connection thomas",

    'summary': "Connection thomas",

    'description': "Connection thomas",

    'author': "Todoo SAS",
    'contributors': ['Pablo Arcos pa@todoo.co'],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Technical Settings',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/connection_cron.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'external_dependencies': {
        'python': ['sshtunnel'],
    },
    'application': True,
}
