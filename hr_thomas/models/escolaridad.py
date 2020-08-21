# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api



class Todoo(models.Model):
    _name = 'escolaridad'
    _rec_name = 'escolaridad_sol'
   
    escolaridad_sol=fields.Char()
    formacion=fields.Selection([('PRIMARIA', 'PRIMARIA'),('BACHILLER', 'BACHILLER'),('CURSO O SEMINARIO', 'CURSO O SEMINARIO'),('TÉCNICA','TÉCNICA'),('TECNOLÓGICA','TECNOLÓGICA'),('UNIVERSITARIA', 'UNIVERSITARIA'),('ESPECIALIZACIÓN', 'ESPECIALIZACIÓN'),('MAESTRÍA','MAESTRÍA'),('DOCTORADO','DOCTORADO')])
    estudia_actualmente=fields.Selection([('SI', 'SI'),('NO', 'NO')])
    nombre_institucion=fields.Char()
    clase_instituto=fields.Selection([('FORMAL(CON CERTIFICADO)', 'FORMAL(CON CERTIFICADO)'),('INFORMAL(SIN CERTIFICADO)', 'INFORMAL(SIN CERTIFICADO)')])
    estado=fields.Selection([('APLAZADO', 'APLAZADO'),('COMPLETADO', 'COMPLETADO'),('INCOMPLETO','INCOMPLETO'),('OTRO','OTRO')])
    pais_estudio=fields.Many2one('res.country')
    tiempo_estudio=fields.Integer()
    periocidad_estudio=fields.Selection([('AÑOS', 'AÑOS'),('CLASES', 'CLASES'),('DÍAS','DÍAS'),('MESES','MESES'),('SEMANAS','SEMANAS'),('SEMESTRES','SEMESTRES')])
    año_grado=fields.Date()
    titulo_obtenido=fields.Many2one('titulo')
    




    
  
  

   
    
    
    