# -*- coding: utf-8 -*-
from . import models
from . import controllers
from odoo import api, SUPERUSER_ID


def _fields_whitelist(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.model.fields'].formbuilder_whitelist('hr.applicant', ['created_user'])


def uninstall_hook(cr, registry):
    """ Deleting all created submenus"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    menus = env['website.menu'].search([])
    for menu in menus:
        if menu.name in ['Aplicar a Vacantes', 'Fase Contratación', 'Descripciones de Cargo', 'Requisiciones']:
            menu.unlink()


