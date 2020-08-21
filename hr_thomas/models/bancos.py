# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api



class Todoo(models.Model):
   _inherit = 'res.partner.bank'

   acc_number = fields.Char(string="Datos Cuenta Bancaria",tracking=True, required="True")
   account_type = fields.Selection([('ahorros', 'AHORROS'),('corriente', 'CORRIENTE')],'Tipo de Cuenta',tracking=True)