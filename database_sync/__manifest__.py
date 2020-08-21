# -*- coding: utf-8 -*-
{
    'name': "Database Sync",

    'summary': """ Sync Two Databases """,
    'description': """Updates Databases Everytime When Records Are Created In Specified Models""",
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Employees',
    'version': '13.0.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base_setup', 'hr_recruitment', 'hr_thomas', 'survey'],

    # always loaded
    'data': ['views/database_details.xml',
             'views/database_sync.xml'],
}
