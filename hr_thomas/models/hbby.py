# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO.

from odoo import fields,models,api



class Todoo(models.Model):
    _name = 'hbby'
    _rec_name = 'nombre_hobby'
    nombre_hobby=fields.Char()

   
    
    
    