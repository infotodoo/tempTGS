# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api



class Todoo(models.Model):
    _name = 'evaluacion'
    _rec_name = 'evaluacion_tiempos_tht'

    #campos activos
    evaluacion_tiempos_tht=fields.Char()
   
   
    