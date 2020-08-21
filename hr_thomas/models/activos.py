# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS

from odoo import fields,models,api



class Todoo(models.Model):
    _name = 'activos'
    _rec_name = 'activo_cargo'

    #campos activos
    categoria=fields.Selection([('FISICO', 'FISICO'),('INFORMACIÓN', 'INFORMACIÓN'),('TECNOLÓGICO','TECNOLÓGICO'),('NO APLICA','NO APLICA')])
    activo_cargo=fields.Text()
    employee_id = fields.Many2one('hr.employee', 'Empleado')
    job_id = fields.Many2one('hr.job', 'Activos')
    cargo_job_id = fields.Char(related="job_id.name")
   
    
    