# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api



class Todoo(models.Model):
    _name = 'centro'
    _rec_name = 'numero'
    centro_costo=fields.Char()
    numero=fields.Char()
    company_id=fields.Many2one('res.company')
    
  

   
    
    
    