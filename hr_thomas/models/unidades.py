# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api



class Todoo(models.Model):
    _name = 'unidades'
    _rec_name = 'nombre_unidad_org'

    nombre_unidad_org = fields.Char()
    company_id=fields.Many2one('res.company')
    
    
    