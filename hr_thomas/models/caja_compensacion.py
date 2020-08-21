from odoo import fields,models,api



class Todoo_arl(models.Model):
    _name = 'caja'
    _rec_name = 'nombre_caja_compensacion'
   
    nombre_caja_compensacion=fields.Char()
    identificador=fields.Char()
    