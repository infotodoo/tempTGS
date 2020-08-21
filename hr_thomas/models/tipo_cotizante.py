from odoo import fields,models,api



class Todoo_tipo_cotizante(models.Model):
    _name = 'tipo.cotizante'
    _rec_name = 'nombre_tipo_cotizante'
   
    nombre_tipo_cotizante=fields.Char()
    