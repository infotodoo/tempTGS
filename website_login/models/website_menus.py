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
            job_menu = records.filtered(lambda l: l.name == 'Jobs')
            menu = [data.name for data in records]
            if 'Aplicar a Vacantes' not in menu and 'Fase Contratación' not in menu and 'Cargos' not in menu and 'Requisiciones' not in menu and 'Descripciones de Cargo' not in menu:
                obj = self.env['website.menu']
                users = [self.env.ref("base.group_portal").id, self.env.ref("base.group_user").id]
                obj.create(
                    {'name': 'Requisiciones', 'website_id': website.id, 'sequence': 99,
                     'parent_id': job_menu.parent_id.id,
                     'url': '/requisiciones', 'group_ids': users})
                obj.create(
                    {'name': 'Descripciones de Cargo', 'website_id': website.id, 'sequence': 100,
                     'parent_id': job_menu.parent_id.id,
                     'url': '/cargos_add', 'group_ids': users})
                obj.create(
                    {'name': 'Aplicar a Vacantes', 'website_id': website.id, 'parent_id': job_menu.id, 'url': '/jobs',
                     'group_ids': users})
                obj.create({'name': 'Fase Contratación', 'website_id': website.id, 'parent_id': job_menu.id,
                            'url': '/applied_jobs', 'group_ids': users})
