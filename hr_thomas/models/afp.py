# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api



class Todoo(models.Model):
    _name = 'afp'
    _rec_name = 'nombre_afp'
   
    nombre_afp=fields.Char()
    identificador=fields.Char()
    
  
  

   
    
    
    