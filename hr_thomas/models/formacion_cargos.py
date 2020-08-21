# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api



class FormacionCargos(models.Model):
    _name = 'formacion.cargos'
    

    #one2many
    # applicant_id = fields.Many2one('hr.applicant', 'Aplicante', tracking=True)
    # employee_id = fields.Many2one('hr.employee', 'Empleado', tracking=True)
    # empleado_asociado=fields.Char(related="employee_id.name")
    #campos formacion
    job_id = fields.Many2one('hr.job', 'Formación', tracking=True)
    formacion_especifica=fields.Char(tracking=True)
    certificado_academico=fields.Selection([('SI', 'SI'),('NO', 'NO')], tracking=True)
    prueba_tecnica=fields.Selection([('SI', 'SI'),('NO', 'NO')],tracking=True)
    certificado_laboral_funciones=fields.Selection([('SI', 'SI'),('NO', 'NO')], tracking=True)  
    
   