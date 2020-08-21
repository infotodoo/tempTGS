# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api
from datetime import datetime
from dateutil import relativedelta


grupo_sanguineo = [

    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-')   
]


class Hijo(models.Model):
    _name = 'hijo'
    _rec_name = 'nombre_hijo'

    #One2many
    applicant_id = fields.Many2one('hr.applicant', 'Aplicante')
    employee_id = fields.Many2one('hr.employee', 'Empleado')
    
    #campos hijos
    nombre_hijo = fields.Char()
    primer_apellido=fields.Char()
    segundo_apellido=fields.Char()
    segundo_nombre=fields.Char()
    fecha_nac_hijo=fields.Date()
    genero_hijo=fields.Selection([('Masculino', 'MASCULINO'),('Femenino', 'FEMENINO')])
    grupo_sanguineo=fields.Selection(grupo_sanguineo)
    nacionalidad=fields.Many2one('res.country')
    pais_nacimiento=fields.Many2one('res.country')
    identificacion=fields.Integer()
    hijastro=fields.Selection([('si', 'SI'),('no', 'NO')])
    ocupacion_hijo=fields.Selection([('EMPLEADO', 'EMPLEADO'),('ESTUDIANTE', 'ESTUDIANTE'),('DESOCUPADO','DESOCUPADO')])
    nivel_escolaridad_hijo=fields.Selection([('PRIMARIA', 'PRIMARIA'),('BACHILLER', 'BACHILLER'),('CURSO O SEMINARIO','CURSO O SEMINARIO'),('TÉCNICA','TÉCNICA'),('TÉCNOLOGICA','TÉCNOLOGICA'),('UNIVERSITARIA','UNIVERSITARIA'),('ESPECIALIZACIÓN','ESPECIALIZACIÓN'),('MAESTRIA','MAESTRÍA'),('DOCTORADO','DOCTORADO')])
    padre_o_madre=fields.Char(related="applicant_id.partner_name")
    padre_madre_emp=fields.Char(related="employee_id.name")
    
    @api.onchange('nombre_hijo','primer_apellido','segundo_apellido','segundo_nombre')
    def _compute_maj_hijo(self):
        self.nombre_hijo = self.nombre_hijo.upper() if self.nombre_hijo else False
        self.primer_apellido = self.primer_apellido.upper() if self.primer_apellido else False
        self.segundo_apellido = self.segundo_apellido.upper() if self.segundo_apellido else False
        self.segundo_nombre = self.segundo_nombre.upper() if self.segundo_nombre else False 

  
        

class Hijos(models.Model):
    _name = 'hijos'
    _rec_name = 'nombre_hijo'

    nombre_hijo = fields.Char()
    primer_apellido=fields.Char()
    segundo_apellido=fields.Char()
    segundo_nombre=fields.Char()
    fecha_nac_hijo=fields.Date()
    genero_hijo=fields.Selection([('Masculino', 'MASCULINO'),('Femenino', 'FEMENINO')])
    grupo_sanguineo=fields.Selection(grupo_sanguineo)
    nacionalidad=fields.Many2one('res.country')
    pais_nacimiento=fields.Many2one('res.country')
    identificacion=fields.Integer()
    hijastro=fields.Selection([('si', 'SI'),('no', 'NO')])