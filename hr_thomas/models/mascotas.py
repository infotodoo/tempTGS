# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api




class Todoo(models.Model):
    _name = 'mascotas'
    _rec_name = 'tipo_mascota'
   
    applicant_id = fields.Many2one('hr.applicant', 'Aplicante')
    employee_id = fields.Many2one('hr.employee', 'Empleado')    
    tipo_mascota=fields.Selection([('AVES', 'AVES'),('CONEJOS', 'CONEJOS'),('GATOS','GATOS'),('HAMSTER','HAMSTER'),('PECES','PECES'),('PERROS','PERROS'),('REPTILES','REPTILES'),('OTROS','OTROS')])   
    
    numero_mascota=fields.Integer()
    dueño_mascota=fields.Char(related="applicant_id.partner_name")
    empleado_dueño_mascota=fields.Char(related="employee_id.name")


   

    