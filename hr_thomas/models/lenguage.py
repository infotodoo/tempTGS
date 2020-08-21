# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api



class Todoo(models.Model):
    _name = 'lenguage'
    _rec_name = 'nombre'
    nombre=fields.Char()
    porcent_dominio=fields.Integer(string="Porcentaje de Dominio")
    po=fields.Integer( related="porcent_dominio")
    applicant_id = fields.Many2one('hr.applicant', 'Aplicante')
    idioma_empleado=fields.Char(related="applicant_id.partner_name")
    employee_id = fields.Many2one('hr.employee', 'Empleado')
    idioma_mod_empleado=fields.Char(related="employee_id.name")

   
    
    
    