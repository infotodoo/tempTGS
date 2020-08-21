# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api



class Todoo(models.Model):
    _name = 'fobias'
    _rec_name = 'name'

    name = fields.Char()
   
    