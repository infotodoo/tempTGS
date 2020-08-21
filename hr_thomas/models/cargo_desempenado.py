# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO.

from odoo import fields,models,api



class Todoo(models.Model):
    _name = 'cargo.desen'
    _rec_name = 'cargo_desempenado'
    cargo_desempenado=fields.Char()

   
    
    