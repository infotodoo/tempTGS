# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api



class Todoo(models.Model):
    _name = 'afc'
    _rec_name = 'nombre_afc'
   
    nombre_afc=fields.Char()
    identificador=fields.Char()
    
  
  

   
    
    
    