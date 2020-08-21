from odoo import fields,models,api



class Todoo_arl(models.Model):
    _name = 'arl'
    _rec_name = 'nombre_arl'
   
    nombre_arl=fields.Char()
    identificador=fields.Char()
    