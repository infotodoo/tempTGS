# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api



class Todoo(models.Model):
  _inherit = 'res.partner'

  identificador = fields.Char('Identificador')
  tipo = fields.Selection([('AFP', 'AFP'),('AFC', 'AFC'),('ARL','ARL'),('EPS','EPS'),('CAJA DE COMPENSACIÓN','CAJA DE COMPENSACIÓN')],tracking=True, string="Clasificación UGPP")