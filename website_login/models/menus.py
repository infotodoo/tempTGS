# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CreateMenu(models.Model):
    _inherit = 'website.menu'

    @api.model
    def _test_function(self):
        websites = self.env['website'].search([])
        menus = self.env['website.menu'].search([])
        for website in websites:
            records = menus.filtered(lambda l: l.website_id.id == website.id)
            for data1 in records:
                print(data1.read())
            job_menu = records.filtered(lambda l: l.name == 'Jobs')
            menu = [data.name for data in records]
            if 'Active Jobs' and 'Applied Jobs' and 'Cargos' not in menu:
                obj = self.env['website.menu']
                users = [self.env.ref("base.group_portal").id, self.env.ref("base.group_user").id]
                obj.create(
                    {'name': 'Cargos', 'website_id': website.id, 'sequence': 100, 'parent_id': job_menu.parent_id.id,
                     'url': '/jobs/add', 'group_ids': users})
                obj.create({'name': 'Active Jobs', 'website_id': website.id, 'parent_id': job_menu.id, 'url': '/jobs',
                            'group_ids': users})
                obj.create({'name': 'Applied Jobs', 'website_id': website.id, 'parent_id': job_menu.id,
                            'url': '/applied_jobs', 'group_ids': users})


class HrApplicantUid(models.Model):
    _inherit = 'hr.applicant'

    created_user = fields.Char()

    def fetch_job_details(self, id):
        obj = self.env['hr.applicant'].with_user(1).browse(id)
        return obj.read()


