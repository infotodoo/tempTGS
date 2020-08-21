# -*- coding: utf-8 -*-
{
    'name': "Website Login",

    'summary': """ Advanced Login For Website """,
    'description': """""",
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Website',
    'version': '13.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base_setup', 'website_hr_recruitment', 'hr_thomas'],

    # always loaded
    'data': ['views/sign_up_form.xml',
             'views/job_apply_form.xml',
             'views/requisiciones.xml',
             'views/requisicion_approval.xml',
             'security/ir.model.access.csv',
             'views/users.xml',
             'views/cargos.xml',
             'views/thank_you.xml',
             'data/website_jobs.xml',
             'views/requisicion_error.xml',
             'views/certificates.xml',
             'views/edit_applied_job.xml'],
    'post_init_hook': '_fields_whitelist',
    'uninstall_hook': 'uninstall_hook',
}
