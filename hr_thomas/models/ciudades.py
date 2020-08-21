# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api



class Todoo(models.Model):
    _name = 'ciudades'
    _rec_name = 'name_city'

    name_city = fields.Char()
    departamentos=fields.Many2one('res.country.state')
    paises=fields.Many2one('res.country')
    
    