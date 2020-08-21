# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api



class Todoo(models.Model):
    _name = 'formacion'
    _rec_name = 'titulo_obtenido'

    #one2many
    applicant_id = fields.Many2one('hr.applicant', 'Aplicante', tracking=True)
    employee_id = fields.Many2one('hr.employee', 'Empleado', tracking=True)
    empleado_asociado=fields.Char(related="employee_id.name")
    #campos formacion
    job_id = fields.Many2one('hr.job', 'Formación', tracking=True)
    formacion_especifica=fields.Char(tracking=True)
    certificado_academico=fields.Selection([('SI', 'SI'),('NO', 'NO')], tracking=True)
    prueba_tecnica=fields.Selection([('SI', 'SI'),('NO', 'NO')],tracking=True)
    certificado_laboral_funciones=fields.Selection([('SI', 'SI'),('NO', 'NO')], tracking=True)  
    general=fields.Selection([('SIN EXPERIENCIA', 'SIN EXPERIENCIA'),('6 MESES', '6 MESES'),('1 AÑO','1 AÑO'),('2 AÑOS','2 AÑOS'),('3 AÑOS','3 AÑOS'),('4 AÑOS','4 AÑOS'),('5 AÑOS','5 AÑOS')])
    especifica_cargos_similares=fields.Selection([('SIN EXPERIENCIA', 'SIN EXPERIENCIA'),('6 MESES', '6 MESES'),('1 AÑO','1 AÑO'),('2 AÑOS','2 AÑOS'),('3 AÑOS','3 AÑOS'),('4 AÑOS','4 AÑOS'),('5 AÑOS','5 AÑOS')])
    objetivo_cargo=fields.Char(tracking=True)    
    #Escala salarial 
    aplica=fields.Selection([('SI', 'SI'),('NO', 'NO')], tracking=True)
    minimo=fields.Float(tracking=True)
    maximo=fields.Float(tracking=True)
    #formacion
    formacion=fields.Selection([('Primaria', 'PRIMARIA'),('Bachiller', 'BACHILLER'),('Curso o Seminario', 'CURSO O SEMINARIO'),('Técnica','TÉCNICA'),('Tecnológica','TECNOLÓGICA'),('Universitaria', 'UNIVERSITARIA'),('Especialización', 'ESPECIALIZACIÓN'),('Maestría','MAESTRÍA'),('Doctorado','DOCTORADO')],tracking=True)
    estudia_actualmente_for=fields.Selection([('SI', 'SI'),('NO', 'NO')], tracking=True)
    nombre_institucion=fields.Char(tracking=True)
    titulo_obtenido=fields.Many2one('titulo', tracking=True)
    clase_titulo=fields.Selection([('FORMAL', 'FORMAL(CON CERTIFICADO)'),('INFORMAL', 'INFORMAL(SIN CERTIFICADO)')])
    estado_formacion=fields.Selection([('APLAZADO', 'APLAZADO'),('COMPLETADO', 'COMPLETADO'),('INCOMPLETO','INCOMPLETO'),('OTRO','OTRO')])
    pais_donde_estudio=fields.Many2one('res.country', tracking=True)
    tiempo_estudio=fields.Integer(tracking=True)
    periocidad_estudio=fields.Selection([('AÑOS', 'AÑOS'),('CLASES', 'CLASES'),('MESES','MESES'),('SEMANAS','SEMANAS'),('SEMESTRES','SEMESTRES'),('DÍAS','DÍAS')])
    fecha_graduacion=fields.Date(tracking=True)
    Empleado_solicitante=fields.Char(related="applicant_id.partner_name")   
    empleado_formacion=fields.Char(related="employee_id.name",tracking=True)


    












