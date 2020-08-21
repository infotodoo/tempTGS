# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api



class Todoo(models.Model):
    _name = 'eps'
    _rec_name = 'nombre_eps'
   
    nombre_eps=fields.Char()
    identificador=fields.Char()
    
  
  

   
    
    
    